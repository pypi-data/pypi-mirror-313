"""Activity Tracker - Monitor and analyze your daily work activities."""

from ._version import __version__
from .tracker import ActivityTracker
from .database import DatabaseHandler

__all__ = ['ActivityTracker', 'DatabaseHandler', '__version__']
