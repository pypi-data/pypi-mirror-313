from datetime import timedelta
from typing import Any, Dict, Optional
from temporalio import workflow as temporal_workflow
from temporalio.workflow import ChildWorkflowCancellationType, ParentClosePolicy
from .observability import logger, log_with_context
import asyncio

temporal_workflow.logger.logger = logger

class WorkflowLogger:
    """Wrapper for workflow logger that ensures proper context and formatting"""
    
    def __init__(self):
        self._logger = temporal_workflow.logger
    
    def _log(self, level: str, message: str, **kwargs: Any):
        if temporal_workflow._Runtime.maybe_current():
            getattr(self._logger, level)(message, extra={'extra_fields': kwargs})
        else:
            log_with_context(level.upper(), message, **kwargs)

    def debug(self, message: str, **kwargs: Any): self._log('debug', message, **kwargs)
    def info(self, message: str, **kwargs: Any): self._log('info', message, **kwargs)
    def warning(self, message: str, **kwargs: Any): self._log('warning', message, **kwargs)
    def error(self, message: str, **kwargs: Any): self._log('error', message, **kwargs)
    def critical(self, message: str, **kwargs: Any): self._log('critical', message, **kwargs)

log = WorkflowLogger()

get_external_workflow_handle = temporal_workflow.get_external_workflow_handle
workflow_info = temporal_workflow.info
continue_as_new = temporal_workflow.continue_as_new
condition = temporal_workflow.wait_condition
import_functions = temporal_workflow.unsafe.imports_passed_through
uuid = temporal_workflow.uuid4

__all__ = [
    'get_external_workflow_handle',
    'workflow_info',
    'continue_as_new',
    'condition',
    'import_functions',
    'log'
    'uuid'
]

class Workflow:
    def defn(self, *args, **kwargs):
        return temporal_workflow.defn(*args, **kwargs)
    def memory(self, fn):
        return temporal_workflow.query(fn)
    def event(self, fn):
        return temporal_workflow.update(fn)
    def run(self, fn):
        return temporal_workflow.run(fn)
    def condition(self, fn):
        return temporal_workflow.wait_condition(fn)
    async def step(self, activity, *args, task_queue: Optional[str] = 'restack', schedule_to_close_timeout: Optional[str] = timedelta(minutes=2), **kwargs):
        input_arg = kwargs.pop('input', None)
        if input_arg is not None:
            args = (*args, input_arg)
        return await temporal_workflow.execute_activity(activity, *args, task_queue=task_queue, schedule_to_close_timeout=schedule_to_close_timeout, **kwargs)
    async def child_start(
            self,
            workflow,
            workflow_id: str,
            input: Optional[Dict[str, Any]] = None,
            task_queue: Optional[str] = 'restack',
            cancellation_type: ChildWorkflowCancellationType = ChildWorkflowCancellationType.WAIT_CANCELLATION_COMPLETED,
            parent_close_policy: ParentClosePolicy = ParentClosePolicy.TERMINATE,
            execution_timeout: Optional[timedelta] = None
        ):
        engine_id = self.get_engine_id_from_client()

        return await temporal_workflow.start_child_workflow(
            workflow=workflow.run,
            args=[input] if input else [],
            id=self.add_engine_id_prefix(engine_id, workflow_id),
            task_queue=task_queue,
            memo={'engineId': engine_id},
            search_attributes={'engineId': [engine_id]},
            cancellation_type=cancellation_type,
            parent_close_policy=parent_close_policy,
            execution_timeout=execution_timeout,
        )

    async def child_execute(
            self,
            workflow,
            workflow_id: str,
            input: Optional[Dict[str, Any]] = None,
            task_queue: Optional[str] = 'restack',
            cancellation_type: ChildWorkflowCancellationType = ChildWorkflowCancellationType.WAIT_CANCELLATION_COMPLETED,
            parent_close_policy: ParentClosePolicy = ParentClosePolicy.TERMINATE,
            execution_timeout: Optional[timedelta] = None
        ):
        engine_id = self.get_engine_id_from_client()

        return await temporal_workflow.execute_child_workflow(
            workflow=workflow.run,
            args=[input] if input else [],
            id=self.add_engine_id_prefix(engine_id, workflow_id),
            task_queue=task_queue,
            memo={'engineId': engine_id},
            search_attributes={'engineId': [engine_id]},
            cancellation_type=cancellation_type,
            parent_close_policy=parent_close_policy,
            execution_timeout=execution_timeout,
        )
    async def sleep(self, seconds: int):
        return await asyncio.sleep(seconds)

    def get_engine_id_from_client(self):
      engineId = temporal_workflow.memo_value('engineId', 'local')
      # log_with_context("INFO", "engineId", engineId=engineId)
      return engineId

    def add_engine_id_prefix(self, engine_id, workflow_id):
        if workflow_id.startswith(f"{engine_id}-"):
            return workflow_id
        return f"{engine_id}-{workflow_id}"

workflow = Workflow()
