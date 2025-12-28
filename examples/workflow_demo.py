"""
Workflow Visualization Demo

Demonstrates the workflow tracking system.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.coordinator import CoordinatorAgent
from rich.console import Console
import webbrowser
from pathlib import Path

console = Console()


def main():
    console.print("[bold cyan]🔄 Workflow Tracking Demo[/bold cyan]\n")
    console.print("This demo shows how the system tracks and visualizes agent workflows.\n")
    
    # Initialize
    coordinator = CoordinatorAgent()
    
    # Example research query
    query = "What are the latest developments in quantum computing?"
    
    console.print(f"[bold]Query:[/bold] {query}\n")
    console.print("Running research workflow...\n")
    
    try:
        # Execute research with workflow tracking
        result = coordinator.research(query, save_report=True)
        
        # Display ASCII workflow
        console.print("\n[bold green]✓ Research Complete![/bold green]\n")
        console.print("[bold]Workflow Visualization:[/bold]\n")
        console.print(result['workflow_diagram'])
        
        # Show report preview
        console.print("\n[bold]Report Preview:[/bold]")
        report_lines = result['report'].split('\n')[:10]
        console.print('\n'.join(report_lines) + '\n...\n')
        
        # Open interactive HTML
        if result.get('workflow_files'):
            html_path = Path(result['workflow_files']['html']).absolute()
            console.print(f"[green]✓[/green] Opening interactive workflow report...")
            console.print(f"[dim]File: {html_path}[/dim]\n")
            
            # Try to open in browser
            try:
                webbrowser.open(f"file://{html_path}")
                console.print("[green]✓[/green] Opened in your default browser!\n")
            except Exception as e:
                console.print(f"[yellow]![/yellow] Could not open browser: {e}")
                console.print(f"[yellow]→[/yellow] Open manually: {html_path}\n")
        
        # Show metrics
        console.print("[bold]Performance Metrics:[/bold]")
        console.print(f"  • Total Duration: {result['metadata']['duration_seconds']:.2f}s")
        console.print(f"  • Research Steps: {result['metadata'].get('research_steps', 0)}")
        
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
    
    finally:
        coordinator.close()
    
    console.print("\n[bold green]Demo complete![/bold green] 🎉\n")


if __name__ == "__main__":
    main()

