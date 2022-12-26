import inspect
from datetime import datetime
from core import SQLiteDatabase

def get_log_type():
    stack = inspect.stack()
    
    return stack[1].function.split('_')[1].upper()

def get_caller_class_name():
    stack = inspect.stack()
    prev_stack_frame = stack[1][0].f_back.f_locals

    if 'self' in prev_stack_frame:
        return prev_stack_frame['self'].__class__.__name__

    if '__file__' in prev_stack_frame:
        #if caller class name is not preset, returns the file name with the relative path
        return prev_stack_frame['__file__'].split('cerebro')[1]

    return "Unknown"

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_event_in_db(event_name, timestamp, message, log_type):
    with SQLiteDatabase() as db:
        db.execute("INSERT INTO event (event_name, timestamp, message, type) VALUES (?, ?, ?, ?)", [event_name, timestamp, message, log_type])

