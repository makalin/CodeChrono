import click
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import time
from typing import Dict, List, Set
import threading
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import box
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import fnmatch
import signal

# Initialize rich console
console = Console()

# File to store the coding time data
DATA_FILE = Path.home() / '.codechrono.json'

# Language detection by file extension
LANGUAGE_EXTENSIONS = {
    'python': ['.py', '.pyx', '.pyi', '.pyw'],
    'javascript': ['.js', '.jsx', '.mjs'],
    'typescript': ['.ts', '.tsx'],
    'java': ['.java'],
    'c++': ['.cpp', '.hpp', '.cc', '.h'],
    'rust': ['.rs'],
    'go': ['.go'],
    'ruby': ['.rb'],
    'php': ['.php'],
    'swift': ['.swift'],
    'kotlin': ['.kt'],
    'html': ['.html', '.htm'],
    'css': ['.css', '.scss', '.sass'],
    'markdown': ['.md', '.markdown'],
}

# Ignore patterns for files and directories
IGNORE_PATTERNS = [
    '.*',           # Hidden files
    '*node_modules*',
    '*venv*',
    '*dist*',
    '*build*',
    '*.git*',
    '*__pycache__*',
    '*.idea*',
    '*.vscode*',
]

class Session:
    def __init__(self, language: str):
        self.language = language
        self.start_time = datetime.now()
        self.last_activity = self.start_time
        self.is_active = True

class CodingTimeTracker(FileSystemEventHandler):
    def __init__(self, watched_dirs: List[str], idle_timeout: int = 300):
        self.watched_dirs = watched_dirs
        self.idle_timeout = idle_timeout  # Time in seconds before session is considered inactive
        self.active_sessions: Dict[str, Session] = {}
        self.data = self.load_data()
        self.observer = Observer()
        self.setup_watchers()
        self.running = True
        
        # Start session cleanup thread
        self.cleanup_thread = threading.Thread(target=self.cleanup_inactive_sessions)
        self.cleanup_thread.daemon = True
        self.cleanup_thread.start()

    def load_data(self) -> Dict:
        if DATA_FILE.exists():
            with open(DATA_FILE) as f:
                return json.load(f)
        return {"sessions": [], "languages": {}}

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def setup_watchers(self):
        """Set up file system watchers for all specified directories."""
        for directory in self.watched_dirs:
            self.observer.schedule(self, directory, recursive=True)

    def should_ignore(self, path: str) -> bool:
        """Check if the file should be ignored based on ignore patterns."""
        path_parts = path.split(os.sep)
        return any(
            any(fnmatch.fnmatch(part, pattern) for pattern in IGNORE_PATTERNS)
            for part in path_parts
        )

    def get_language(self, file_path: str) -> str:
        """Detect programming language based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        for language, extensions in LANGUAGE_EXTENSIONS.items():
            if ext in extensions:
                return language
        return "other"

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory or self.should_ignore(event.src_path):
            return

        language = self.get_language(event.src_path)
        if language == "other":
            return

        current_time = datetime.now()
        
        # Update or create session
        if language in self.active_sessions:
            self.active_sessions[language].last_activity = current_time
        else:
            self.active_sessions[language] = Session(language)
            console.print(f"[green]Started tracking {language}[/green]")

    def cleanup_inactive_sessions(self):
        """Periodically check for and cleanup inactive sessions."""
        while self.running:
            current_time = datetime.now()
            for language in list(self.active_sessions.keys()):
                session = self.active_sessions[language]
                if (current_time - session.last_activity).total_seconds() > self.idle_timeout:
                    self.end_session(language)
            time.sleep(60)  # Check every minute

    def end_session(self, language: str):
        """End a coding session for a specific language."""
        if language not in self.active_sessions:
            return

        session = self.active_sessions[language]
        duration = (session.last_activity - session.start_time).total_seconds() / 3600

        # Only record sessions that are longer than 1 minute
        if duration * 60 > 1:
            session_data = {
                "language": language,
                "start_time": session.start_time.isoformat(),
                "end_time": session.last_activity.isoformat(),
                "duration": duration
            }
            self.data["sessions"].append(session_data)

            if language not in self.data["languages"]:
                self.data["languages"][language] = {"total_hours": 0, "sessions": 0}

            self.data["languages"][language]["total_hours"] += duration
            self.data["languages"][language]["sessions"] += 1
            self.save_data()

            console.print(f"[yellow]Ended {language} session ({duration:.2f} hours)[/yellow]")

        del self.active_sessions[language]

    def stop(self):
        """Stop the tracker and cleanup."""
        self.running = False
        for language in list(self.active_sessions.keys()):
            self.end_session(language)
        self.observer.stop()
        self.observer.join()

@click.group()
def cli():
    """Automatically track your coding time across different programming languages."""
    pass

@cli.command()
@click.argument('directories', nargs=-1, type=click.Path(exists=True))
@click.option('--idle-timeout', default=300, help='Seconds of inactivity before ending a session')
def watch(directories, idle_timeout):
    """Start watching directories for coding activity."""
    if not directories:
        directories = [os.getcwd()]

    console.print(f"[green]Watching directories:[/green]")
    for directory in directories:
        console.print(f"- {directory}")

    tracker = CodingTimeTracker(directories, idle_timeout)
    tracker.observer.start()

    def handle_shutdown(signum, frame):
        console.print("\n[yellow]Shutting down...[/yellow]")
        tracker.stop()
        exit(0)

    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tracker.stop()

@cli.command()
def status():
    """Show current tracking status."""
    data = CodingTimeTracker([]).data
    active_sessions = [s for s in data.get("sessions", []) if "end_time" not in s]
    
    if not active_sessions:
        console.print("[yellow]No active coding sessions[/yellow]")
        return

    table = Table(title="Active Sessions")
    table.add_column("Language")
    table.add_column("Duration")
    table.add_column("Last Activity")

    for session in active_sessions:
        start_time = datetime.fromisoformat(session["start_time"])
        duration = datetime.now() - start_time
        table.add_row(
            session["language"],
            str(duration).split('.')[0],
            start_time.strftime("%H:%M:%S")
        )

    console.print(table)

@cli.command()
@click.option('--days', default=7, help='Number of days to show statistics for')
def stats(days):
    """Show coding statistics."""
    data = CodingTimeTracker([]).data
    
    if not data["languages"]:
        console.print("[yellow]No coding sessions recorded yet[/yellow]")
        return
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Filter recent sessions
    recent_sessions = [
        s for s in data["sessions"]
        if datetime.fromisoformat(s["start_time"]) > cutoff_date
    ]
    
    # Calculate recent statistics
    recent_stats = {}
    for session in recent_sessions:
        language = session["language"]
        if language not in recent_stats:
            recent_stats[language] = {"total_hours": 0, "sessions": 0}
        
        recent_stats[language]["total_hours"] += session["duration"]
        recent_stats[language]["sessions"] += 1
    
    # Create statistics table
    table = Table(title=f"Coding Statistics (Last {days} days)")
    table.add_column("Language", style="cyan")
    table.add_column("Total Hours", justify="right")
    table.add_column("Sessions", justify="right")
    table.add_column("Avg Hours/Session", justify="right")
    
    for lang, stats in sorted(recent_stats.items(), key=lambda x: x[1]["total_hours"], reverse=True):
        avg_hours = stats["total_hours"] / stats["sessions"]
        table.add_row(
            lang.capitalize(),
            f"{stats['total_hours']:.2f}",
            str(stats["sessions"]),
            f"{avg_hours:.2f}"
        )
    
    console.print(table)
    
    # Show all-time totals
    total_hours = sum(lang["total_hours"] for lang in data["languages"].values())
    total_sessions = sum(lang["sessions"] for lang in data["languages"].values())
    
    console.print("\n[bold]All-time totals:[/bold]")
    console.print(f"Total hours coded: [cyan]{total_hours:.2f}[/cyan]")
    console.print(f"Total sessions: [cyan]{total_sessions}[/cyan]")

if __name__ == '__main__':
    cli()
