"""
Coordinator Agent that orchestrates research and writing workflows.
"""

import time
from datetime import datetime
from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent
from src.utils.workflow import WorkflowTracker, WorkflowStepType
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.research_agent import create_research_agent
from utils.config import get_openai_api_key


class CoordinatorAgent(BaseAgent):
    """Coordinates research and writing agents."""
    
    def __init__(self, workflow_tracker: Optional[WorkflowTracker] = None):
        super().__init__("coordinator", workflow_tracker)
        self.api_key = get_openai_api_key()
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        # Initialize agents
        self.research_agent = create_research_agent(self.api_key)
        # For now, we'll use research_agent for writing too
        # In a full implementation, you'd have a separate writer agent
        self.writer_agent = self.research_agent
    
    def research(self, query: str, save_report: bool = True, **kwargs) -> Dict[str, Any]:
        """
        Main entry point for research workflow with tracking.
        """
        # CREATE WORKFLOW TRACKER
        tracker = WorkflowTracker(f"Research: {query[:50]}")
        tracker.add_step(
            WorkflowStepType.START,
            "coordinator",
            "Initialize workflow"
        )
        
        start_time = time.time()
        
        # Step 1: Research Phase
        tracker.add_step(
            WorkflowStepType.AGENT_CALL,
            "coordinator",
            "Delegate to Research Agent"
        )
        
        research_start = time.time()
        try:
            research_result = self.research_agent.invoke({"input": query})
            research_duration = time.time() - research_start
            
            # Extract metadata from research result
            steps = research_result.get("intermediate_steps", [])
            research_output = research_result.get("output", "")
            
            tracker.add_step(
                WorkflowStepType.RESULT,
                "research",
                "Research completed",
                details={"steps": len(steps)},
                duration=research_duration
            )
        except Exception as e:
            research_duration = time.time() - research_start
            tracker.add_step(
                WorkflowStepType.ERROR,
                "research",
                f"Research failed: {str(e)}",
                duration=research_duration
            )
            tracker.complete()
            return {
                "query": query,
                "error": str(e),
                "workflow": tracker.to_json(),
                "workflow_diagram": tracker.generate_ascii_diagram(),
                "metadata": {
                    "duration_seconds": time.time() - start_time,
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        # Step 2: Writing Phase (simplified - using research agent)
        tracker.add_step(
            WorkflowStepType.AGENT_CALL,
            "coordinator",
            "Generate report"
        )
        
        writer_start = time.time()
        try:
            # For now, we'll format the research output as a report
            report_content = f"# Research Report: {query}\n\n{research_output}"
            writer_duration = time.time() - writer_start
            
            tracker.add_step(
                WorkflowStepType.RESULT,
                "writer",
                "Report generated",
                details={"saved": save_report},
                duration=writer_duration
            )
        except Exception as e:
            writer_duration = time.time() - writer_start
            tracker.add_step(
                WorkflowStepType.ERROR,
                "writer",
                f"Report generation failed: {str(e)}",
                duration=writer_duration
            )
        
        # Complete workflow
        tracker.complete()
        tracker.add_step(
            WorkflowStepType.END,
            "coordinator",
            "Workflow complete"
        )
        
        # Save workflow visualization
        workflow_files = None
        try:
            workflow_files = tracker.save_workflow()
        except Exception as e:
            print(f"Warning: Could not save workflow: {e}")
        
        # Calculate total time
        duration = time.time() - start_time
        
        return {
            "query": query,
            "report": report_content,
            "research_findings": research_output,
            "workflow": tracker.to_json(),
            "workflow_diagram": tracker.generate_ascii_diagram(),
            "workflow_files": workflow_files,
            "metadata": {
                "duration_seconds": duration,
                "research_steps": len(steps),
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def close(self):
        """Clean up resources."""
        pass

