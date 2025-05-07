# ⏱️ CodeChrono

**CodeChrono** is an advanced coding time tracker designed to help developers understand and optimize their workflow. By monitoring file changes, CodeChrono provides detailed insights into your coding habits, enabling better time management and productivity.

## Features

- **Real-time Monitoring**: Tracks coding activity in real time.
- **Rich Output**: Interactive and visually appealing CLI using the `rich` library.
- **File System Watching**: Monitors file changes using `watchdog`.
- **Detailed Reports**: Summarizes daily, weekly, and project-specific coding activity.
- **Multithreaded**: Ensures seamless performance without blocking operations.
- **JSON-based Storage**: Saves and loads activity logs in a simple, human-readable format.
- **Web Dashboard**: Beautiful web interface for visualizing coding activity.
- **Export Options**: Export data in JSON or CSV format.
- **Type Hints**: Full type annotation support for better code maintainability.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/makalin/CodeChrono.git
   cd CodeChrono
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

1. Start tracking your coding activity:
   ```bash
   python -m codechrono.cli.commands start
   ```

2. View activity summary:
   ```bash
   python -m codechrono.cli.commands summary
   ```

3. Export activity data:
   ```bash
   python -m codechrono.cli.commands export --format json
   ```

### Advanced Usage

1. Track specific directories:
   ```bash
   python -m codechrono.cli.commands start --watch /path/to/project1 /path/to/project2
   ```

2. Use custom configuration:
   ```bash
   python -m codechrono.cli.commands start --config custom_config.json
   ```

3. View activity for specific time period:
   ```bash
   python -m codechrono.cli.commands summary --days 30
   ```

4. Export to specific file:
   ```bash
   python -m codechrono.cli.commands export --format csv --output activity_report.csv
   ```

### Web Dashboard

1. Start the web server:
   ```bash
   python -m codechrono.web.app
   ```

2. Open your browser and navigate to `http://localhost:5000`

## Configuration

The default configuration file (`config.json`) supports the following options:

```json
{
    "watch_paths": [
        "/path/to/project1",
        "/path/to/project2"
    ],
    "exclude_patterns": [
        "*.pyc",
        "__pycache__",
        ".git"
    ]
}
```

## Development

### Running Tests

```bash
pytest
```

### Type Checking

```bash
mypy codechrono
```

### Code Formatting

```bash
black codechrono
```

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature-name'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

CodeChrono leverages powerful libraries like:
- `click` for building the command-line interface.
- `rich` for enhanced console output.
- `watchdog` for file system monitoring.
- `flask` for the web dashboard.
- `chart.js` for data visualization.

Thank you to all the developers and contributors of these libraries for making this project possible.
