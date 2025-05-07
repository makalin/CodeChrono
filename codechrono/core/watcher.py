"""
File system watching functionality for CodeChrono.

This module handles monitoring file system changes using watchdog.
"""

from pathlib import Path
from typing import Callable, List, Optional, Set
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

logger = logging.getLogger(__name__)

class CodeChangeHandler(FileSystemEventHandler):
    """
    Handles file system events for code changes.
    
    Attributes:
        callback (Callable): Function to call when changes are detected
        exclude_patterns (Set[str]): Patterns to exclude from monitoring
    """
    
    def __init__(self, callback: Callable[[Path, str], None], exclude_patterns: Optional[Set[str]] = None) -> None:
        """
        Initialize the change handler.
        
        Args:
            callback: Function to call with (file_path, event_type)
            exclude_patterns: Set of patterns to exclude from monitoring
        """
        self.callback = callback
        self.exclude_patterns = exclude_patterns or set()
        
    def on_any_event(self, event: FileSystemEvent) -> None:
        """
        Handle any file system event.
        
        Args:
            event: The file system event that occurred
        """
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Skip excluded files
        if any(pattern in str(file_path) for pattern in self.exclude_patterns):
            return
            
        if event.event_type in ["created", "modified", "deleted"]:
            self.callback(file_path, event.event_type)
            
class FileWatcher:
    """
    Watches directories for file changes.
    
    Attributes:
        observer (Observer): Watchdog observer instance
        handler (CodeChangeHandler): Event handler instance
    """
    
    def __init__(self, callback: Callable[[Path, str], None], exclude_patterns: Optional[Set[str]] = None) -> None:
        """
        Initialize the file watcher.
        
        Args:
            callback: Function to call when changes are detected
            exclude_patterns: Set of patterns to exclude from monitoring
        """
        self.observer = Observer()
        self.handler = CodeChangeHandler(callback, exclude_patterns)
        
    def start_watching(self, paths: List[Path]) -> None:
        """
        Start watching the specified paths.
        
        Args:
            paths: List of paths to watch
        """
        for path in paths:
            if not path.exists():
                logger.warning(f"Path does not exist: {path}")
                continue
                
            self.observer.schedule(self.handler, str(path), recursive=True)
            logger.info(f"Started watching: {path}")
            
        self.observer.start()
        
    def stop_watching(self) -> None:
        """Stop watching all paths."""
        self.observer.stop()
        self.observer.join()
        logger.info("Stopped watching all paths") 