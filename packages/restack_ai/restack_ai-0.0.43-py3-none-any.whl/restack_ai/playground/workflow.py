from datetime import timedelta
from temporalio import workflow
from dataclasses import dataclass
from typing import Any

@dataclass
class PlaygroundInput:
    functionName: str
    taskQueue: str
    input: Any

@workflow.defn(name="playgroundRun")
class playgroundRun:
    @workflow.run
    async def run(self, params: PlaygroundInput):
        result = await workflow.execute_activity(
            activity=params.functionName,
            task_queue=params.taskQueue,
            args=[params.input],
            start_to_close_timeout=timedelta(seconds=120)
        )
        return result