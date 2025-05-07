"""
Command-line interface for CodeChrono.

This module provides the CLI commands for interacting with CodeChrono.
"""

import click
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta

from ..core.tracker import ActivityTracker
from ..core.watcher import FileWatcher

console = Console()

@click.group()
def cli() -> None:
    """CodeChrono - Advanced coding time tracker."""
    pass

@cli.command()
@click.option('--config', '-c', type=click.Path(), help='Path to config file')
@click.option('--watch', '-w', multiple=True, type=click.Path(), help='Paths to watch')
def start(config: Optional[str], watch: tuple) -> None:
    """
    Start tracking coding activity.
    
    Args:
        config: Path to configuration file
        watch: Paths to watch for changes
    """
    config_path = Path(config) if config else None
    tracker = ActivityTracker(config_path)
    
    watch_paths = [Path(p) for p in watch] if watch else [Path.cwd()]
    
    def on_change(file_path: Path, event_type: str) -> None:
        tracker.track_file_change(file_path, event_type)
        
    watcher = FileWatcher(on_change)
    watcher.start_watching(watch_paths)
    
    console.print("[bold green]CodeChrono started![/bold green]")
    console.print("Press Ctrl+C to stop tracking...")
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        watcher.stop_watching()
        console.print("\n[bold yellow]Tracking stopped.[/bold yellow]")

@cli.command()
@click.option('--days', '-d', type=int, default=7, help='Number of days to show')
def summary(days: int) -> None:
    """
    Show summary of coding activity.
    
    Args:
        days: Number of days to include in summary
    """
    tracker = ActivityTracker()
    start_time = datetime.now() - timedelta(days=days)
    summary = tracker.get_activity_summary(start_time)
    
    table = Table(title=f"Coding Activity Summary (Last {days} days)")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Files", str(summary["total_files"]))
    table.add_row("Total Events", str(summary["total_events"]))
    
    console.print(table)
    
    if summary["file_activity"]:
        file_table = Table(title="File Activity")
        file_table.add_column("File", style="cyan")
        file_table.add_column("Changes", style="green")
        
        for file_path, changes in summary["file_activity"].items():
            file_table.add_row(file_path, str(changes))
            
        console.print(file_table)

@cli.command()
@click.option('--format', '-f', type=click.Choice(['json', 'csv']), default='json', help='Export format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def export(format: str, output: Optional[str]) -> None:
    """
    Export coding activity data.
    
    Args:
        format: Export format (json or csv)
        output: Output file path
    """
    tracker = ActivityTracker()
    output_path = Path(output) if output else None
    tracker.export_data(format, output_path)
    console.print(f"[bold green]Data exported successfully![/bold green]")

if __name__ == '__main__':
    cli() 