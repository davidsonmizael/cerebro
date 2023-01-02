from core.db import SQLiteDatabase

def get_frequency(task_name):
    with SQLiteDatabase() as db:
        result = db.execute_fetchone("SELECT frequency FROM task WHERE name = ?", [task_name])
    
    if result:
        return result[0]

def update_task_status(task_name, status):
    with SQLiteDatabase() as db:
        db.execute("UPDATE task SET last_run_date = datetime('now', 'localtime'), status = ? WHERE name = ?", [status, task_name])

def insert_task_run(task_name, start_time, status, additional_info):
    with SQLiteDatabase() as db:
        db.execute("INSERT INTO task_run (task_name, start_date, end_date, status, additional_info) VALUES (?, ?, datetime('now', 'localtime'), ?, ?)", [task_name, start_time, status, additional_info])

def get_task_config(task_name, config_name):
    with SQLiteDatabase() as db:
        result = db.execute_fetchone("SELECT config_value FROM task_config WHERE task_name = ? AND config_name = ?", [task_name, config_name])
    
    if result:
        return result[0]