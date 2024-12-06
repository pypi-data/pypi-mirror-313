import time
import shutil
from datetime import datetime
from colorama import init, Fore, Style
from Quartz.CoreGraphics import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)
from pynput import mouse, keyboard
from mac_activity_tracker.database import DatabaseHandler
from mac_activity_tracker.config import CODING_APPS, TALKING_APPS, IDLE_TIMEOUT, DB_PATH, DEBUG

class ActivityTracker:
    def __init__(self):
        self.db = DatabaseHandler(DB_PATH)
        self.last_activity_time = datetime.now()
        self.last_window = None
        self.current_activity_start = datetime.now()
        self.current_activity_type = None
        init()  # Initialize colorama
        self.terminal_width = shutil.get_terminal_size().columns
        
        # Setup activity monitors
        self.mouse_listener = mouse.Listener(on_move=self.on_activity)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        
    def on_activity(self, *args):
        self.last_activity_time = datetime.now()

    def get_active_window(self):
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        for window in window_list:
            # Check for both layer 0 and owner name to filter out system windows
            if (window.get('kCGWindowLayer', 0) == 0 and 
                window.get('kCGWindowOwnerName') not in ['Window Server', '']):
                app_name = window.get('kCGWindowOwnerName', '')
                if DEBUG:
                    print(f"Window Info: {dict(window)}")  # Debug window properties
                return app_name
        return None

    def get_activity_type(self, window_name):
        if not window_name:
            return 'other'
        if window_name in CODING_APPS:
            return 'coding'
        if window_name in TALKING_APPS:
            return 'talking'
        return 'other'

    def is_idle(self):
        idle_duration = (datetime.now() - self.last_activity_time).total_seconds()
        return idle_duration > IDLE_TIMEOUT

    def log_current_activity(self):
        if self.current_activity_type:
            end_time = datetime.now()
            self.db.log_activity(
                self.current_activity_type,
                self.current_activity_start,
                end_time
            )
            self.current_activity_start = end_time

    def start(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()

        try:
            print("Activity tracking started. Press Ctrl+C to stop.")
            while True:
                current_window = self.get_active_window()
                
                if self.is_idle():
                    new_activity_type = 'idle'
                else:
                    new_activity_type = self.get_activity_type(current_window)

                # Log activity if type changed
                if new_activity_type != self.current_activity_type:
                    self.log_current_activity()
                    self.current_activity_type = new_activity_type

                # Always log current activity to keep stats current
                self.log_current_activity()

                # Update display every second
                summary, total_time = self.db.get_summary()
                if total_time > 0:
                    stats = {
                        'coding': summary.get('coding', 0),
                        'talking': summary.get('talking', 0),
                        'other': summary.get('other', 0),
                        'idle': summary.get('idle', 0)
                    }
                    
                    # Calculate percentages
                    percentages = {k: (v / total_time) * 100 for k, v in stats.items()}
                    
                    # Convert seconds to hours and minutes for display
                    def format_time(seconds):
                        h = seconds // 3600
                        m = (seconds % 3600) // 60
                        return f"{h:02d}h {m:02d}m"

                    # Clear line and create separator
                    print('\r' + ' ' * self.terminal_width, end='')
                    print('\r' + Style.BRIGHT + '─' * self.terminal_width + Style.RESET_ALL)
                    
                    # Show current activity (with extra clearing)
                    print('\r' + ' ' * self.terminal_width, end='')
                    activity_colors = {
                        'coding': Fore.GREEN,
                        'talking': Fore.CYAN,
                        'other': Fore.YELLOW,
                        'idle': Fore.RED
                    }
                    current_color = activity_colors.get(self.current_activity_type, Fore.WHITE)
                    print(f"\r{Style.BRIGHT}Current Activity: {current_color}{self.current_activity_type.upper()}{Style.RESET_ALL}")
                    
                    # Show statistics
                    # Format each stat differently based on debug mode
                    def format_stat(activity, percentage, seconds):
                        time_str = format_time(seconds)
                        if DEBUG:
                            return f"{percentage:5.1f}% ({time_str} - {seconds}s)"
                        return f"{percentage:5.1f}% ({time_str})"
                        
                    stats_line = (
                        f"{Fore.GREEN}Coding: {format_stat(stats['coding'], percentages['coding'], stats['coding'])} {Style.RESET_ALL}| "
                        f"{Fore.CYAN}Talking: {format_stat(stats['talking'], percentages['talking'], stats['talking'])} {Style.RESET_ALL}| "
                        f"{Fore.YELLOW}Other: {format_stat(stats['other'], percentages['other'], stats['other'])} {Style.RESET_ALL}| "
                        f"{Fore.RED}Idle: {format_stat(stats['idle'], percentages['idle'], stats['idle'])}{Style.RESET_ALL}"
                    )
                    print(f"\r{stats_line}")
                    
                    # Bottom separator
                    print(Style.BRIGHT + '─' * self.terminal_width + Style.RESET_ALL, end='', flush=True)
                    
                    # Move cursor up 3 lines to overwrite on next update
                    print('\033[3A', end='')

                time.sleep(1)  # Check every second

        except KeyboardInterrupt:
            self.log_current_activity()
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            print("\n\n")  # Add newline after interrupt

    def print_summary(self):
        summary, total_time = self.db.get_summary()
        print("\nToday's Activity Summary:")
        for activity_type, duration in summary.items():
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            percentage = (duration / total_time * 100) if total_time > 0 else 0
            print(f"{activity_type}: {hours}h {minutes}m ({percentage:.1f}%)")

def main():
    tracker = ActivityTracker()
    tracker.start()

if __name__ == '__main__':
    main()
