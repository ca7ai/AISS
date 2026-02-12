"""
AISS CLI interface
"""
import click
import asyncio
from rich.console import Console
from typing import Optional
from ..core.scanner import SecurityScanner

console = Console()

@click.group()
def cli():
    """AISS - AI Security Screener"""
    pass

@cli.command()
@click.argument('target', required=False)
@click.option('--type', '-t', type=click.Choice(['moltbook', 'openclaw', 'custom']), 
              help='Type of agent to test')
@click.option('--agent-id', help='Agent ID for Moltbook/OpenClaw agents')
@click.option('--output', '-o', help='Output file for results')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'html']), default='text')
def scan(target: Optional[str], type: str, agent_id: str, output: str, format: str):
    """Scan an AI agent for security issues"""
    try:
        if not target and not agent_id:
            if type == 'moltbook':
                console.print("[red]Error: Need --agent-id for Moltbook agents[/red]")
                return
            elif type == 'openclaw':
                console.print("[yellow]No target specified, switching to self-check mode[/yellow]")
                self_check()
                return
            else:
                console.print("[red]Error: Need either target URL or --agent-id[/red]")
                return

        # Construct proper target URL
        if type == 'moltbook' and agent_id:
            target = f"https://www.moltbook.com/agents/{agent_id}"
        elif type == 'openclaw' and agent_id:
            # Use OpenClaw's agent endpoint
            target = f"http://localhost:3000/agents/{agent_id}"

        scanner = SecurityScanner(target)
        results = asyncio.run(scanner.run_scan())
        
        # Generate and save/display report
        # ... (rest of the reporting logic)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@cli.command()
@click.option('--output', '-o', help='Output file for results')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'html']), default='text')
def self_check(output: Optional[str] = None, format: str = 'text'):
    """Run security self-check on this agent"""
    try:
        console.print("[bold blue]Starting self-check...[/bold blue]")
        
        scanner = SecurityScanner()
        results = asyncio.run(scanner.run_self_check())
        
        # ... (reporting logic)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == '__main__':
    cli()