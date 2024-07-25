import time
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class EventManager:
    def __init__(self, default_interval=0.1, mode='debounce'):
        self.default_interval = default_interval
        self.mode = mode
        self.last_event_times = {}
        self.is_throttled = {}
        self.functions = []
        self.priority_functions = []

    def add_function(self, func, interval=None, priority=False):
        if priority:
            self.priority_functions.append(func)
        else:
            self.functions.append({
                'function': func,
                'interval': interval if interval is not None else self.default_interval
            })
            self.last_event_times[func] = 0
            self.is_throttled[func] = False

    def execute_function(self, func, event):
        def threaded_func():
            try:
                func(event)
            except Exception as e:
                logging.error(f"Error executing function {func.__name__}: {e}")

        threading.Thread(target=threaded_func).start()

    def handle_event(self, event):
        current_time = time.time()

        # Execute priority functions immediately
        for func in self.priority_functions:
            self.execute_function(func, event)
            
        for func_entry in self.functions:
            func = func_entry['function']
            interval = func_entry['interval']

            if self.mode == 'debounce':
                if current_time - self.last_event_times[func] >= interval:
                    self.last_event_times[func] = current_time
                    self.execute_function(func, event)

            elif self.mode == 'throttle':
                if not self.is_throttled[func]:
                    self.is_throttled[func] = True
                    self.execute_function(func, event)
                    threading.Timer(interval, self.reset_throttle, [func]).start()

    def reset_throttle(self, func):
        self.is_throttled[func] = False
class EventAPI:
    def __init__(self, event_manager):
        self.event_manager = event_manager

    def bind_event(self, widget, event_name):
        widget.bind(event_name, self.event_manager.handle_event)

    def add_function(self, func, interval=None, priority=False):
        self.event_manager.add_function(func, interval, priority)
