"""
Base Agent class with workflow tracking support.
"""

from typing import Optional, Dict
from src.utils.workflow import WorkflowTracker, WorkflowStepType


class BaseAgent:
    """Base class for all agents with workflow tracking."""
    
    def __init__(self, agent_name: str, workflow_tracker: Optional[WorkflowTracker] = None):
        self.agent_name = agent_name
        self.workflow_tracker = workflow_tracker
    
    def _track_step(
        self,
        step_type: WorkflowStepType,
        action: str,
        details: Optional[Dict] = None,
        result: Optional[str] = None,
        duration: Optional[float] = None
    ):
        """Track workflow step if tracker is available."""
        if self.workflow_tracker:
            self.workflow_tracker.add_step(
                step_type=step_type,
                agent=self.agent_name,
                action=action,
                details=details,
                result=result,
                duration=duration
            )

