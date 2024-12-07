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
        engineId = workflow.memo_value("engineId", "local")
        result = await workflow.execute_activity(
            activity=params.functionName,
            task_queue=f"{engineId}-{params.taskQueue}",
            args=[params.input],
            start_to_close_timeout=timedelta(seconds=120),
        )
        return result
