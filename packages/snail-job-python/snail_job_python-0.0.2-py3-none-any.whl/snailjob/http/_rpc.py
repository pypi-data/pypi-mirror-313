import json
import urllib
from typing import Any

from ..cfg import SNAIL_HEADERS, SNAIL_SERVER_HOST, SNAIL_SERVER_PORT
from ..log import SnailLog
from ..schemas import NettyResult, SnailJobRequest, StatusEnum


def send_to_server(uri: str, payload: Any, job_name: str) -> StatusEnum:
    """发送请求到程服务器"""
    request = SnailJobRequest.build(args=[payload])
    req = urllib.request.Request(
        url=f"http://{SNAIL_SERVER_HOST}:{SNAIL_SERVER_PORT}{uri}",
        data=json.dumps(request.model_dump(mode="json")).encode("utf-8"),
        headers=SNAIL_HEADERS,
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode("utf-8"))
        serverResponse = NettyResult(**data)
        assert request.reqId == serverResponse.reqId, "reqId 不一致的!"
        if serverResponse.status == StatusEnum.YES:
            SnailLog.LOCAL.info(f"{job_name}成功: reqId={request.reqId}")
            try:
                SnailLog.LOCAL.debug(f"data={payload.model_dump(mode='json')}")
            except:
                SnailLog.LOCAL.debug(f"data={payload}")
        else:
            SnailLog.LOCAL.error(f"{job_name}失败: {serverResponse.message}")
        return serverResponse.status
    except urllib.error.URLError as ex:
        SnailLog.LOCAL.error(f"无法连接服务器: {ex}")
        return StatusEnum.NO
