from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class WorkflowEvent:
    name: str
    input: Optional[Dict[str, Any]] = None

@dataclass
class SendWorkflowEvent:
    event: WorkflowEvent
    workflow: Optional[str] = None