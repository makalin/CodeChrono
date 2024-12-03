# CodeChrono

**CodeChrono** is an advanced coding time tracker designed to help developers understand and optimize their workflow. By monitoring file changes, CodeChrono provides detailed insights into your coding habits, enabling better time management and productivity.

## Features

- **Real-time Monitoring**: Tracks coding activity in real time.
- **Rich Output**: Interactive and visually appealing CLI using the `rich` library.
- **File System Watching**: Monitors file changes using `watchdog`.
- **Detailed Reports**: Summarizes daily, weekly, and project-specific coding activity.
- **Multithreaded**: Ensures seamless performance without blocking operations.
- **JSON-based Storage**: Saves and loads activity logs in a simple, human-readable format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/codechrono.git
   cd codechrono
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start tracking your coding activity:
   ```bash
   python codechrono.py
   ```

2. Use the CLI options for specific tasks:
   - View a summary of your coding activity.
   - Configure file monitoring paths.

3. Stop tracking anytime using Ctrl+C.

## Configuration

- The default configuration monitors your current working directory.
- To customize, edit the `config.json` file.

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

Thank you to all the developers and contributors of these libraries for making this project possible.
