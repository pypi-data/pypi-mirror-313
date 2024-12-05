import atexit
import logging
import logging.handlers
import os
import pathlib
import queue
import sys
import threading
import time
import traceback
from typing import Any, List, Optional

BASE_DIR = pathlib.Path(os.getcwd()).resolve()

from .cfg import (
    SNAIL_GROUP_NAME,
    SNAIL_HOST_IP,
    SNAIL_HOST_PORT,
    SNAIL_LOG_FORMAT,
    SNAIL_LOG_LEVEL,
    SNAIL_LOG_LOCAL_BACKUP_COUNT,
    SNAIL_LOG_LOCAL_FILENAME,
    SNAIL_LOG_REMOTE_BUFFER_SIZE,
    SNAIL_LOG_REMOTE_INTERVAL,
    SNAIL_NAMESPACE,
)
from .ctx import SnailContextManager
from .schemas import JobLogTask, TaskLogFieldDTO


class SnailHttpHandler(logging.Handler):
    """基于时间滑动窗口、队列缓存的日期处理器，用于远程上报日志"""

    # 日志格式转换规则
    RECORD_MAPPINGS = (
        ("time_stamp", lambda r: str(int(r.created * 1000))),
        ("level", lambda r: r.levelname),
        ("thread", lambda r: r.threadName),
        ("message", lambda r: r.msg),
        ("location", lambda r: f"{r.module}:{r.funcName}:{r.lineno}"),
        ("throwable", lambda r: SnailHttpHandler._format_exc_info(r.exc_info)),
    )

    def __init__(self, capacity=2, interval=10):
        super().__init__()
        self.lock = threading.RLock()
        self.capacity = capacity
        self.interval = interval
        self.buffer = queue.Queue(capacity)
        self.timer = None
        self._start_timer()

    def emit(self, record: logging.LogRecord):
        with self.lock:
            # 1. 转化日志元素
            dto = SnailHttpHandler._transform(record)

            # 2. 如果当前缓冲区为空，启动计时器
            if self.buffer.empty():
                self._start_timer()

            # 3. 将日志存放到缓冲区
            self.buffer.put(dto)

            # 4. 如果缓冲区满，则冲洗
            if self.buffer.full():
                self.flush()

    def flush(self):
        """冲洗缓冲区，并发送到远程服务器"""
        items: List[JobLogTask] = []
        while not self.buffer.empty():
            items.append(self.buffer.get())

        if items:
            self._send(items)

    def close(self):
        if self.timer:
            self.timer.cancel()
        self.flush()
        super().close()

    def _format_exc_info(exc_info: Any) -> Optional[str]:
        if exc_info is None:
            return None
        etype, value, tb = exc_info
        errors = traceback.format_exception(etype, value, tb)
        # 删除当前函数(execute_wrapper)的调用栈
        errors.pop(1)
        return "\n".join(errors)

    @staticmethod
    def _transform(record: logging.LogRecord) -> JobLogTask:
        """转换日志结构

        Args:
            record (logging.LogRecord): logging标准日志结构

        Returns:
            JobLogTask: SnailJob 服务器日志格式
        """

        field_list: List[TaskLogFieldDTO] = []
        for key, mapper in SnailHttpHandler.RECORD_MAPPINGS:
            assert callable(mapper), "Mapper is not callable"
            field_list.append(TaskLogFieldDTO(name=key, value=mapper(record)))
        field_list.append(TaskLogFieldDTO(name="host", value=SNAIL_HOST_IP))
        field_list.append(TaskLogFieldDTO(name="port", value=SNAIL_HOST_PORT))

        log_context = SnailContextManager.get_log_context()
        job_log_task = JobLogTask(
            logType="JOB",
            namespaceId=SNAIL_NAMESPACE,
            groupName=SNAIL_GROUP_NAME,
            realTime=int(time.time() * 1000),
            fieldList=field_list,
            jobId=log_context.jobId,
            taskBatchId=log_context.taskBatchId,
            taskId=log_context.taskId,
        )

        return job_log_task

    def _send(self, items: List[JobLogTask]):
        """推送日志到远程服务器

        Args:
            items (List[JobLogTask]): 日志元素
        """
        # 延迟import, 解决循环依赖
        from .rpc import send_batch_log_report

        send_batch_log_report(items)

    def _start_timer(self):
        """启动时间滑动窗口定时器"""

        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.interval, self.flush)
        self.timer.start()


class SnailLog:
    """Snail Job 日志门面"""

    LOCAL = logging.getLogger("SnailJob Local Logger")
    REMOTE = logging.getLogger("SnailJob Remote Logger")

    @staticmethod
    def config_loggers():
        # 全局日志格式化器
        formatter = logging.Formatter(SNAIL_LOG_FORMAT)

        # 创建日志目录
        (BASE_DIR / SNAIL_LOG_LOCAL_FILENAME).resolve().parent.mkdir(
            parents=True, exist_ok=True
        )
        # handler: 文件
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=BASE_DIR / SNAIL_LOG_LOCAL_FILENAME,
            when="d",
            backupCount=SNAIL_LOG_LOCAL_BACKUP_COUNT,
        )
        file_handler.setFormatter(formatter)

        # handler: 控制台
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        # handler: http
        http_handler = SnailHttpHandler(
            capacity=SNAIL_LOG_REMOTE_BUFFER_SIZE,
            interval=SNAIL_LOG_REMOTE_INTERVAL,
        )
        # 程序退出时关闭 handler
        atexit.register(lambda: http_handler.close())

        SnailLog.REMOTE.setLevel(SNAIL_LOG_LEVEL)
        SnailLog.REMOTE.parent = None
        SnailLog.REMOTE.addHandler(file_handler)
        SnailLog.REMOTE.addHandler(http_handler)
        SnailLog.REMOTE.addHandler(stream_handler)

        SnailLog.LOCAL.setLevel(SNAIL_LOG_LEVEL)
        SnailLog.LOCAL.parent = None
        SnailLog.LOCAL.addHandler(file_handler)
        SnailLog.LOCAL.addHandler(stream_handler)


# 配置日志
SnailLog.config_loggers()
