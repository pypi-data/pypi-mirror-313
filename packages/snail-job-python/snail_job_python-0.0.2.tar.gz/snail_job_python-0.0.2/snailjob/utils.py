import json
from typing import Any, List

from .cfg import ROOT_MAP
from .ctx import SnailContextManager
from .err import SnailJobError
from .log import SnailLog
from .rpc import send_batch_map_report
from .schemas import ExecuteResult, MapTaskRequest, StatusEnum


def mr_do_map(taskList: List[Any], nextTaskName: str) -> ExecuteResult:
    """MapReduce 的 Map 阶段帮助函数，上报分片结果给服务器

    Args:
        taskList (List[Any]): Map任务列表
        nextTaskName (str):  下一个任务

    Raises:
        SnailJobError: 校验参数参数

    Returns:
        ExecuteResult: 执行结果
    """
    job_context = SnailContextManager.get_job_context()

    if not nextTaskName:
        raise SnailJobError("The next task name can not empty")

    if not taskList:
        raise SnailJobError(f"The task list can not empty {nextTaskName}")

    if len(taskList) > 200:
        raise SnailJobError(
            f"[{nextTaskName}] map task size is too large, network maybe overload... please try to split the tasks."
        )

    if ROOT_MAP == nextTaskName:
        raise SnailJobError(f"The Next taskName can not be {ROOT_MAP}")

    wf_context = (
        json.dumps(job_context.changeWfContext) if job_context.changeWfContext else ""
    )
    request = MapTaskRequest(
        jobId=job_context.jobId,
        taskBatchId=job_context.taskBatchId,
        parentId=job_context.taskId,
        workflowTaskBatchId=job_context.workflowTaskBatchId,
        workflowNodeId=job_context.workflowNodeId,
        wfContext=wf_context,
        taskName=nextTaskName,
        subTask=taskList,
    )

    if send_batch_map_report(request) == StatusEnum.YES:
        SnailLog.LOCAL.info(
            f"Map task create successfully!. taskName:[{nextTaskName}] TaskId:[{job_context.taskId}]"
        )
    else:
        raise SnailJobError(f"Map failed for task: {nextTaskName}")

    return ExecuteResult.success()
