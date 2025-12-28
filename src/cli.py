"""
Command-line interface with workflow visualization.
"""

from rich.console import Console
from rich.markdown import Markdown
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.coordinator import CoordinatorAgent


console = Console()


def interactive_mode():
    """Run interactive CLI mode."""
    console.print("[bold cyan]🔄 Research Agent with Workflow Tracking[/bold cyan]\n")
    console.print("Type your research queries. Type 'exit' or 'quit' to stop.\n")
    
    coordinator = CoordinatorAgent()
    
    try:
        while True:
            query = input("You: ").strip()
            
            if query.lower() in ['exit', 'quit']:
                console.print("\n[bold green]Goodbye![/bold green]")
                break
            
            if not query:
                continue
            
            try:
                # Execute research with workflow tracking
                result = coordinator.research(query, save_report=True)
                
                # Display results
                console.print("\n" + "="*70 + "\n")
                console.print(Markdown(result['report']))
                console.print("\n" + "="*70 + "\n")
                
                # Display workflow visualization (NEW!)
                if 'workflow_diagram' in result:
                    console.print("\n[bold cyan]📊 Workflow Visualization:[/bold cyan]\n")
                    console.print(result['workflow_diagram'])
                    console.print()
                
                # Display metadata
                meta = result['metadata']
                console.print(
                    f"[dim]Completed in {meta['duration_seconds']:.2f}s | "
                    f"Research steps: {meta.get('research_steps', 0)}[/dim]\n"
                )
                
                # Show workflow files location (NEW!)
                if result.get('workflow_files'):
                    console.print(
                        f"[dim]📁 Workflow saved:[/dim]\n"
                        f"[dim]  • HTML Report: {result['workflow_files']['html']}[/dim]\n"
                        f"[dim]  • JSON Data: {result['workflow_files']['json']}[/dim]\n"
                    )
                
            except Exception as e:
                console.print(f"[red]✗ Error:[/red] {e}\n")
    
    finally:
        coordinator.close()


def main():
    """Main entry point."""
    interactive_mode()


if __name__ == "__main__":
    main()

