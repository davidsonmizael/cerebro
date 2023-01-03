import importlib, inspect
from threading import Thread
from core.logger import EventLogger
from datetime import datetime
import time
from core.util.task_util import *

class TaskController(Thread):

    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        tasks = self.get_tasks()
        while True:
            for task in tasks:
                name, cls, obj, frequency = task['name'], task['class'], task['obj'], task['frequency']
                
                now = datetime.now()
                run_now = check_if_now_matches_expr(now, frequency)
                
                if not run_now:
                    EventLogger.log_debug(f"[Controller][{name}] NOW doesn't match expression:  {now} - {frequency}")
                    continue

                if (obj and obj.is_alive()) or get_task_status(name) == 'RUNNING':
                    EventLogger.log_debug(f"[Controller][{name}] Task still running")
                    continue
                
                if obj and not obj.is_alive() and get_task_status(name) in ['FAILED', 'COMPLETED']:
                    obj = None

                if not obj:
                    obj = cls()

                EventLogger.log_info(f"[Controller][{name}] Starting task")
                obj.start()
                
            time.sleep(30)

    def get_tasks(self):
        threads = []
        for name, cls in inspect.getmembers(importlib.import_module("core.task.impl"), inspect.isclass):
            EventLogger.log_info(f"[Controller] Task found: {name}")
            obj = cls()
            threads.append({
                "name": name,
                "class": cls,
                "obj":  obj,
                "frequency": obj.frequency
            })
        
        return threads