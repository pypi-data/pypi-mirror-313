import sqlite3
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity_type TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    duration INTEGER
                )
            ''')

    def log_activity(self, activity_type, start_time, end_time):
        duration = int((end_time - start_time).total_seconds())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO activity_logs (activity_type, start_time, end_time, duration)
                VALUES (?, ?, ?, ?)
            ''', (activity_type, start_time, end_time, duration))

    def get_summary(self, start_date=None):
        if not start_date:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT activity_type, SUM(duration)
                FROM activity_logs
                WHERE start_time >= ?
                GROUP BY activity_type
            ''', (start_date,))
            summary = dict(cursor.fetchall())
            
            # Get total time
            cursor = conn.execute('''
                SELECT SUM(duration)
                FROM activity_logs
                WHERE start_time >= ?
            ''', (start_date,))
            total_time = cursor.fetchone()[0] or 0
            
            return summary, total_time
