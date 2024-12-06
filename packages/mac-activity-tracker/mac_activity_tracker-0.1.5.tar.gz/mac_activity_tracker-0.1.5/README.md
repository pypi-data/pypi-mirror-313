# Mac Activity Tracker

A simple and efficient work activity tracking application for macOS that helps you monitor and manage your daily work activities.

## Features

- Track time spent on different activities
- Automatic categorization of applications (coding, talking, other)
- Idle time detection
- Activity summaries and reports
- Simple and intuitive interface

## Installation

You can install Activity Tracker directly from PyPI:

```bash
pip install mac-activity-tracker
```

Or install from source:

```bash
git clone https://github.com/yourusername/mac-activity-tracker.git
cd mac-activity-tracker
pip install -e .
```

## Usage

Start tracking your activities:

```bash
mac-activity-tracker
```

This will begin monitoring your activity and display real-time statistics. Press Ctrl+C to stop tracking and see a summary.

## Configuration

The default configuration can be found in `mac_activity_tracker/config.py`. You can modify:

- CODING_APPS: List of applications considered as coding activity
- TALKING_APPS: List of applications considered as communication
- IDLE_TIMEOUT: Time in seconds before considering the system idle
- DB_PATH: Location of the SQLite database file

## Development

To set up the development environment:

```bash
git clone https://github.com/yourusername/mac-activity-tracker.git
cd mac-activity-tracker
pip install -e ".[dev]"
```

## License

See the [LICENSE](LICENSE) file for details.
