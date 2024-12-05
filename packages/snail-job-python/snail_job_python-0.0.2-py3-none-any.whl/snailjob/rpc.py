from typing import List

from .cfg import SNAIL_USE_GRPC
from .schemas import (
    DispatchJobResult,
    JobLogTask,
    MapTaskRequest,
    SnailJobRequest,
    StatusEnum,
)

if SNAIL_USE_GRPC:
    from .grpc import send_to_server
else:
    from .http import send_to_server


def send_heartbeat():
    """注册客户端(心跳)"""
    URI = "/beat"
    payload = SnailJobRequest.build(["PING"])
    return send_to_server(URI, payload.model_dump(), "发送心跳")


def send_dispatch_result(payload: DispatchJobResult) -> StatusEnum:
    """执行结果上报"""
    URI = "/report/dispatch/result"
    return send_to_server(URI, payload.model_dump(), "结果上报")


def send_batch_log_report(payload: List[JobLogTask]) -> StatusEnum:
    """日志批量上报"""
    URI = "/batch/server/report/log"
    return send_to_server(URI, [log.model_dump() for log in payload], "日志批量上报")


def send_batch_map_report(payload: MapTaskRequest) -> StatusEnum:
    """生成同步MAP任务"""
    URI = "/batch/report/job/map/task/v1"
    return send_to_server(URI, payload.model_dump(), "生成同步MAP任务")
