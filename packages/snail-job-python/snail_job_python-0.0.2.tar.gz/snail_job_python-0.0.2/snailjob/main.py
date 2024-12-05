import asyncio
import threading
import time

from .cfg import SNAIL_HOST_IP, SNAIL_HOST_PORT, SNAIL_USE_GRPC
from .grpc import run_grpc_server
from .http import run_http_server
from .log import SnailLog
from .rpc import send_heartbeat


class HeartbeatTask:
    """心跳发送任务"""

    def __init__(self) -> None:
        self._thread = threading.Thread(target=self._send_heartbeats, daemon=True)
        self.event = threading.Event()

    def _send_heartbeats(self):
        while not self.event.is_set():
            send_heartbeat()
            time.sleep(28)

    def run(self):
        self._thread.start()


if SNAIL_USE_GRPC:

    def client_main():
        """客户端主函数"""
        heartbeat_task = HeartbeatTask()
        heartbeat_task.run()
        run_grpc_server(SNAIL_HOST_IP, SNAIL_HOST_PORT)

else:

    def client_main():
        """客户端主函数"""
        heartbeat_task = HeartbeatTask()
        heartbeat_task.run()
        try:
            asyncio.run(run_http_server(SNAIL_HOST_IP, SNAIL_HOST_PORT))
        except KeyboardInterrupt:
            SnailLog.LOCAL.info("KeyboardInterrupt, 退出程序")
        except Exception as ex:
            heartbeat_task.event.set()
            SnailLog.LOCAL.error(f"程序发生异常，正在退出: {ex}")
