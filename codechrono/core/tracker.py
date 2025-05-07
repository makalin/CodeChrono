"""
Core tracking functionality for CodeChrono.

This module handles the tracking of coding activity, including file changes,
time tracking, and activity logging.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import json
import logging

logger = logging.getLogger(__name__)

class ActivityTracker:
    """
    Tracks coding activity across multiple files and projects.
    
    Attributes:
        activity_log (Dict): Dictionary storing activity data
        watched_files (Set[Path]): Set of files being monitored
        start_time (datetime): When tracking began
    """
    
    def __init__(self, config_path: Optional[Path] = None) -> None:
        """
        Initialize the activity tracker.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.activity_log: Dict = {}
        self.watched_files: Set[Path] = set()
        self.start_time: datetime = datetime.now()
        self.config_path = config_path or Path("config.json")
        self._load_config()
        
    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_path.exists():
                with open(self.config_path) as f:
                    self.config = json.load(f)
            else:
                self.config = {"watch_paths": [], "exclude_patterns": []}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            self.config = {"watch_paths": [], "exclude_patterns": []}
            
    def track_file_change(self, file_path: Path, event_type: str) -> None:
        """
        Record a file change event.
        
        Args:
            file_path: Path to the changed file
            event_type: Type of change (created, modified, deleted)
        """
        timestamp = datetime.now().isoformat()
        if file_path not in self.activity_log:
            self.activity_log[file_path] = []
            
        self.activity_log[file_path].append({
            "timestamp": timestamp,
            "event_type": event_type
        })
        logger.info(f"Tracked {event_type} event for {file_path}")
        
    def get_activity_summary(self, start_time: Optional[datetime] = None) -> Dict:
        """
        Generate a summary of coding activity.
        
        Args:
            start_time: Optional start time for filtering activity
            
        Returns:
            Dictionary containing activity summary
        """
        summary = {
            "total_files": len(self.activity_log),
            "total_events": sum(len(events) for events in self.activity_log.values()),
            "file_activity": {}
        }
        
        for file_path, events in self.activity_log.items():
            if start_time:
                events = [e for e in events if datetime.fromisoformat(e["timestamp"]) >= start_time]
            summary["file_activity"][str(file_path)] = len(events)
            
        return summary
        
    def export_data(self, format: str = "json", output_path: Optional[Path] = None) -> None:
        """
        Export activity data to a file.
        
        Args:
            format: Export format (json, csv)
            output_path: Path to save the export file
        """
        if not output_path:
            output_path = Path(f"codechrono_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}")
            
        if format == "json":
            with open(output_path, "w") as f:
                json.dump(self.activity_log, f, indent=2)
        elif format == "csv":
            import csv
            with open(output_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["file_path", "timestamp", "event_type"])
                for file_path, events in self.activity_log.items():
                    for event in events:
                        writer.writerow([file_path, event["timestamp"], event["event_type"]])
        else:
            raise ValueError(f"Unsupported export format: {format}")
            
        logger.info(f"Exported activity data to {output_path}") 