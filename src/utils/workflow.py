"""
Workflow Visualization System

Tracks agent workflows and generates multiple visualization formats.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
from pathlib import Path


class WorkflowStepType(Enum):
    """Types of workflow steps."""
    START = "start"
    END = "end"
    AGENT_CALL = "agent_call"
    TOOL_USE = "tool_use"
    RESULT = "result"
    ERROR = "error"
    DECISION = "decision"


class WorkflowStep:
    """Represents a single step in a workflow."""
    
    def __init__(
        self,
        step_type: WorkflowStepType,
        agent: str,
        action: str,
        details: Optional[Dict] = None,
        result: Optional[str] = None,
        duration: Optional[float] = None,
        timestamp: Optional[datetime] = None
    ):
        self.step_type = step_type
        self.agent = agent
        self.action = action
        self.details = details or {}
        self.result = result
        self.duration = duration
        self.timestamp = timestamp or datetime.now()
        self.step_id = len(WorkflowTracker._instances) if hasattr(WorkflowTracker, '_instances') else 0
    
    def to_dict(self) -> Dict:
        """Convert step to dictionary."""
        return {
            "step_id": self.step_id,
            "type": self.step_type.value,
            "agent": self.agent,
            "action": self.action,
            "details": self.details,
            "result": self.result,
            "duration": self.duration,
            "timestamp": self.timestamp.isoformat()
        }


class WorkflowTracker:
    """Tracks workflow steps and generates visualizations."""
    
    _instances = []
    
    def __init__(self, workflow_name: str):
        self.workflow_name = workflow_name
        self.steps: List[WorkflowStep] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.completed = False
        WorkflowTracker._instances.append(self)
    
    def add_step(
        self,
        step_type: WorkflowStepType,
        agent: str,
        action: str,
        details: Optional[Dict] = None,
        result: Optional[str] = None,
        duration: Optional[float] = None
    ):
        """Add a step to the workflow."""
        if not self.start_time:
            self.start_time = datetime.now()
        
        step = WorkflowStep(
            step_type=step_type,
            agent=agent,
            action=action,
            details=details,
            result=result,
            duration=duration
        )
        step.step_id = len(self.steps)
        self.steps.append(step)
    
    def complete(self):
        """Mark workflow as complete."""
        self.completed = True
        self.end_time = datetime.now()
    
    def get_duration(self) -> float:
        """Get total workflow duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        elif self.start_time:
            return (datetime.now() - self.start_time).total_seconds()
        return 0.0
    
    def to_json(self) -> Dict:
        """Convert workflow to JSON format."""
        return {
            "workflow_name": self.workflow_name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.get_duration(),
            "completed": self.completed,
            "steps": [step.to_dict() for step in self.steps]
        }
    
    def generate_ascii_diagram(self) -> str:
        """Generate ASCII diagram of the workflow."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"WORKFLOW: {self.workflow_name}")
        lines.append(f"Duration: {self.get_duration():.2f}s")
        lines.append("=" * 70)
        lines.append("")
        
        step_icons = {
            WorkflowStepType.START: "🚀",
            WorkflowStepType.END: "🏁",
            WorkflowStepType.AGENT_CALL: "🤖",
            WorkflowStepType.TOOL_USE: "🔧",
            WorkflowStepType.RESULT: "✅",
            WorkflowStepType.ERROR: "❌",
            WorkflowStepType.DECISION: "🤔"
        }
        
        for i, step in enumerate(self.steps, 1):
            icon = step_icons.get(step.step_type, "•")
            lines.append(f"{i}. {icon} [{step.agent}] {step.action}")
            
            if step.details:
                for key, value in step.details.items():
                    lines.append(f"   ├─ {key}: {value}")
            
            if step.duration:
                lines.append(f"   └─ Duration: {step.duration:.2f}s")
            elif step.result:
                lines.append(f"   └─ Result: {step.result[:50]}...")
            
            lines.append("")
        
        # Summary
        lines.append("=" * 70)
        lines.append("SUMMARY:")
        step_counts = {}
        for step in self.steps:
            step_counts[step.step_type.value] = step_counts.get(step.step_type.value, 0) + 1
        
        for step_type, count in step_counts.items():
            lines.append(f"  • {step_type}: {count}")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def generate_mermaid_diagram(self) -> str:
        """Generate Mermaid diagram format."""
        lines = ["graph TD"]
        
        for i, step in enumerate(self.steps):
            node_id = f"step{i}"
            label = f"{step.agent}: {step.action[:30]}"
            lines.append(f'    {node_id}["{label}"]')
            
            if i > 0:
                prev_id = f"step{i-1}"
                lines.append(f"    {prev_id} --> {node_id}")
        
        return "\n".join(lines)
    
    def save_workflow(self, output_dir: str = "output/workflows") -> Dict[str, str]:
        """Save workflow in multiple formats."""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"workflow_{timestamp}"
        
        files = {}
        
        # Save JSON
        json_path = os.path.join(output_dir, f"{base_name}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_json(), f, indent=2)
        files['json'] = json_path
        
        # Save ASCII
        txt_path = os.path.join(output_dir, f"{base_name}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_ascii_diagram())
        files['txt'] = txt_path
        
        # Save Mermaid
        mmd_path = os.path.join(output_dir, f"{base_name}.mmd")
        with open(mmd_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_mermaid_diagram())
        files['mmd'] = mmd_path
        
        # Save HTML
        html_path = os.path.join(output_dir, f"{base_name}.html")
        html_content = self._generate_html_report()
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        files['html'] = html_path
        
        return files
    
    def _generate_html_report(self) -> str:
        """Generate interactive HTML report."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Workflow: {self.workflow_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .step {{
            margin: 15px 0;
            padding: 15px;
            border-left: 4px solid #4CAF50;
            background: #f9f9f9;
        }}
        .step-header {{
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }}
        .step-details {{
            margin-left: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        .summary {{
            margin-top: 30px;
            padding: 15px;
            background: #e8f5e9;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Workflow: {self.workflow_name}</h1>
        <p><strong>Duration:</strong> {self.get_duration():.2f}s</p>
        <p><strong>Status:</strong> {'Completed' if self.completed else 'In Progress'}</p>
        
        <h2>Steps</h2>
"""
        
        for i, step in enumerate(self.steps, 1):
            html += f"""
        <div class="step">
            <div class="step-header">Step {i}: {step.action}</div>
            <div class="step-details">
                <p><strong>Agent:</strong> {step.agent}</p>
                <p><strong>Type:</strong> {step.step_type.value}</p>
"""
            if step.duration:
                html += f"<p><strong>Duration:</strong> {step.duration:.2f}s</p>"
            if step.details:
                html += "<p><strong>Details:</strong></p><ul>"
                for key, value in step.details.items():
                    html += f"<li>{key}: {value}</li>"
                html += "</ul>"
            if step.result:
                html += f"<p><strong>Result:</strong> {step.result[:100]}...</p>"
            
            html += """
            </div>
        </div>
"""
        
        # Summary
        step_counts = {}
        for step in self.steps:
            step_counts[step.step_type.value] = step_counts.get(step.step_type.value, 0) + 1
        
        html += """
        <div class="summary">
            <h2>Summary</h2>
            <ul>
"""
        for step_type, count in step_counts.items():
            html += f"<li>{step_type}: {count}</li>"
        
        html += """
            </ul>
        </div>
    </div>
</body>
</html>
"""
        return html

