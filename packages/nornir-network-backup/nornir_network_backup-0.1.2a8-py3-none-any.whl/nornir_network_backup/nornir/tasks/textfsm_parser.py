from ntc_templates.parse import parse_output
from nornir.core.task import Result, Task

import logging

logger = logging.getLogger(__name__)


def task_textfsm(task: Task, cmd: str, data: str) -> Result:
    """task to apply textfsm template to the output of the command

    This task should never fail because we don't want it to stop the workflow.
    """
    result = None
    changed = False
    try:
        result = parse_output(platform=task.host.platform, command=cmd, data=data)
        changed = True
    except Exception:
        logger.error(
            f"unable to parse textfsm for host:{task.host.name} platform:{task.host.platform} command:{cmd}"
        )
        pass

    return Result(host=task.host, result=result, failed=False, changed=changed)
