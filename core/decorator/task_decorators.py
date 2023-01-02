from functools import wraps
from datetime import datetime
from util.task_util import *
from util.event_logger_util import *
from core import EventLogger
import traceback

def monitor_task(func):
    @wraps(func)
    def wrapper(*args, **kw):
        task_name = func.__qualname__.split('.')[0]
        additional_info = None
        status = 'RUNNING'
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res = None

        update_task_status(task_name, status)
        try:
            res = func(*args, **kw)
            status = 'COMPLETED'
            update_task_status(task_name, status)
        except Exception as e:
            status = 'FAILED'
            additional_info = "".join(traceback.TracebackException.from_exception(e).format())
            EventLogger.log_error("Task failed.", additional_info)
            update_task_status(task_name, status)
        finally:
            insert_task_run(task_name, start_time, status, additional_info)

        return res
    return wrapper