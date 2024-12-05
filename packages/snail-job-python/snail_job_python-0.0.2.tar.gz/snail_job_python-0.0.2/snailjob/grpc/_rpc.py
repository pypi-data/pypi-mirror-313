import json
from typing import Any

import grpc

from ..cfg import SNAIL_HEADERS, SNAIL_SERVER_HOST, SNAIL_SERVER_PORT
from ..log import SnailLog
from ..schemas import SnailJobRequest, StatusEnum
from . import snailjob_pb2, snailjob_pb2_grpc


def send_to_server(uri: str, payload: Any, job_name: str) -> StatusEnum:
    """发送请求到程服务器"""
    request = SnailJobRequest.build(args=[payload])
    try:
        with grpc.insecure_channel(
            f"{SNAIL_SERVER_HOST}:{SNAIL_SERVER_PORT}"
        ) as channel:
            stub = snailjob_pb2_grpc.UnaryRequestStub(channel)
            req = snailjob_pb2.GrpcSnailJobRequest(
                reqId=request.reqId,
                metadata=snailjob_pb2.Metadata(
                    uri=uri,
                    headers=SNAIL_HEADERS,
                ),
                body=json.dumps([payload]),
            )
            response = stub.unaryRequest(req)
            assert request.reqId == response.reqId, "reqId 不一致的!"
            if response.status == StatusEnum.YES:
                SnailLog.LOCAL.info(f"{job_name}成功: reqId={request.reqId}")
                try:
                    SnailLog.LOCAL.debug(f"data={payload.model_dump(mode='json')}")
                except:
                    SnailLog.LOCAL.debug(f"data={payload}")
            else:
                SnailLog.LOCAL.error(f"{job_name}失败: {response.message}")
            return response.status
    except grpc.RpcError as ex:
        SnailLog.LOCAL.error(f"无法连接服务器: {ex}")
