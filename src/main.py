import click
import os
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.core.generator import TestGenerator

console = Console()

@click.command()
@click.option('--req', prompt='Paste your requirement', help='The requirement text to analyze.')
def main(req):
    """AI Test Case Generator: Requirements to Gherkin & Structured Test Cases"""
    
    console.print(Panel("[bold blue]🤖 AI is analyzing your requirement...[/bold blue]"))
    
    try:
        # Initialize the generator and invoke the AI
        gen = TestGenerator()
        result = gen.generate_from_text(req)

        # 1. Display Generated Gherkin
        console.print("\n[bold green]✅ Generated Gherkin Feature:[/bold green]")
        console.print(Panel(result.gherkin_feature, style="italic green"))

        # 2. Display Structured Test Case Table
        table = Table(title="Structured Test Cases", show_header=True, header_style="bold magenta")
        table.add_column("Priority", style="dim", width=10)
        table.add_column("Title", style="cyan")
        table.add_column("Type", style="green")

        for tc in result.test_cases:
            table.add_row(tc.priority, tc.title, tc.test_type)
        
        console.print(table)
        console.print(f"\n[bold yellow]Target Coverage Score:[/bold yellow] {result.coverage_score}%")

        # 3. Export Logic (Production Ready)
        os.makedirs("data/output", exist_ok=True)
        
        # Save Gherkin File
        gherkin_path = os.path.join("data/output", "generated_test.feature")
        with open(gherkin_path, "w") as f:
            f.write(result.gherkin_feature)
        
        # Save JSON Data (for Jira/TestRail integration)
        json_path = os.path.join("data/output", "test_data.json")
        with open(json_path, "w") as f:
            json_data = [tc.model_dump() for tc in result.test_cases]
            json.dump(json_data, f, indent=4)

        console.print("\n---")
        console.print(f"[bold cyan]💾 Files Exported successfully:[/bold cyan]")
        console.print(f"  • Gherkin: [underline]{gherkin_path}[/underline]")
        console.print(f"  • JSON:    [underline]{json_path}[/underline]")

    except Exception as e:
        console.print(f"[bold red]Error during generation:[/bold red] {str(e)}")

if __name__ == '__main__':
    main()
