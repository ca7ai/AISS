"""
AISS Command Line Interface
"""
import click
import asyncio
import json
from rich.console import Console
from rich.table import Table
from typing import Optional
import os
from ..core.scanner import SecurityScanner
from datetime import datetime

console = Console()

def print_findings(findings):
    table = Table(title="Security Findings")
    
    table.add_column("Severity", style="bold")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Remediation")
    
    for finding in findings:
        table.add_row(
            finding.severity.value,
            finding.title,
            finding.description,
            finding.remediation
        )
    
    console.print(table)

@click.group()
def cli():
    """AISS - AI Security Screener"""
    pass

@cli.command()
@click.argument('target_url', required=False)
@click.option('--output', '-o', help='Output file for results')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'html']), default='text')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def scan(target_url: Optional[str], output: Optional[str], format: str, verbose: bool):
    """Run security scan on target agent"""
    try:
        if verbose:
            console.print("[bold blue]Starting security scan...[/bold blue]")
            
        scanner = SecurityScanner(target_url)
        results = asyncio.run(scanner.run_scan())
        
        if format == 'text':
            print_findings(results['findings'])
        elif format == 'json':
            if output:
                with open(output, 'w') as f:
                    json.dump(results, f, indent=2)
            else:
                print(json.dumps(results, indent=2))
        elif format == 'html':
            # TODO: Implement HTML report generation
            pass
            
        if verbose:
            console.print("[bold green]Scan complete![/bold green]")
            
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()

@cli.command()
def self_check():
    """Run security self-check"""
    try:
        console.print("[bold blue]Starting self-check...[/bold blue]")
        scanner = SecurityScanner()
        results = asyncio.run(scanner.run_scan())
        print_findings(results['findings'])
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    cli()