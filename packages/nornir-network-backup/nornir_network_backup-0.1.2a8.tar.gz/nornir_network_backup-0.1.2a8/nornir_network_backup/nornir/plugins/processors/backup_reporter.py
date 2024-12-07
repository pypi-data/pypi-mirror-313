# note that these imports are only needed if you are annotating your code with types
# from typing import Dict

# from nornir.core import Nornir
from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, MultiResult, Task


class BackupReporter:
    def task_started(self, task: Task) -> None:
        print(f">>> starting task: {task.name}")

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        print(f">>> completed task: {task.name}")

    def task_instance_started(self, task: Task, host: Host) -> None:
        print(f">>> starting instance of task: {task.name}")

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        print(f">>> completed instance of task: {task.name}")
        print(f"  - {host.name}: - {result.result}")

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        print(f">>> starting subtask instance of task: {task.name}")

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        print(f">>> completed subtask instance of task: {task.name}")
