import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from aiohttp import web
from aiohttp.web_request import Request

from ..log import SnailLog
from ..schemas import (
    DispatchJobRequest,
    NettyResult,
    SnailJobRequest,
    StatusEnum,
    StopJobRequest,
)

DISPATCHER_THREAD_POOL_EXECUTOR = ThreadPoolExecutor(
    thread_name_prefix=f"snail-job-dispatcher",
)


async def handle_dispatch(request: Request):
    from ..exec import ExecutorManager

    """处理任务调度"""
    data = await request.json()
    serverRequest = SnailJobRequest(**data)
    assert len(serverRequest.args) > 0, "SnailJobRequest.args 不能为空"

    dispatchJobRequest = DispatchJobRequest(**serverRequest.args[0])
    SnailLog.LOCAL.info(f"接收到的任务执行请求: reqId={serverRequest.reqId}")
    # 需要创建线程，才可以设置 context 并使用 SnailLog
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        DISPATCHER_THREAD_POOL_EXECUTOR,
        partial(ExecutorManager.dispatch, dispatchJobRequest),
    )
    return web.json_response(
        NettyResult(
            status=result.status,
            reqId=serverRequest.reqId,
            data=result.data,
            message=result.message,
        ).model_dump(mode="json")
    )


async def handle_stop(request: Request):
    from ..exec import ExecutorManager

    """处理任务停止"""
    data = await request.json()
    serverRequest = SnailJobRequest(**data)
    assert len(serverRequest.args) > 0, "SnailJobRequest.args 不能为空"

    stopJobRequest = StopJobRequest(**serverRequest.args[0])
    SnailLog.LOCAL.info(f"接收到的任务停止请求: reqId={serverRequest.reqId}")
    ExecutorManager.stop(stopJobRequest)

    return web.json_response(
        NettyResult(
            status=StatusEnum.YES,
            reqId=serverRequest.reqId,
            data=True,
        ).model_dump(mode="json")
    )


async def run_http_server(host: str, port: int):
    """web server 协程"""
    app = web.Application()

    # 定义端点处理器
    app.router.add_post("/job/dispatch/v1", handle_dispatch)
    app.router.add_post("/job/stop/v1", handle_stop)

    # 启动aio服务器
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()
    SnailLog.LOCAL.info(f"启动 client-side 服务器成功({host}:{port})")
    # 等待服务器启动
    while True:
        await asyncio.sleep(1)
