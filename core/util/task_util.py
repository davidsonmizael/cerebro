from core.db import PostgresConnector

def get_frequency(task_name):
    with PostgresConnector() as db:
        result = db.execute_select("SELECT frequency FROM task WHERE name = %s", [task_name], fetch_one=True)
    
    if result:
        return result[0]

def update_task_status(task_name, status):
    with PostgresConnector() as db:
        db.execute_update("UPDATE task SET last_run_date = now(), status = %s WHERE name = %s", [status, task_name])

def insert_task_run(task_name, start_time, status, additional_info):
    with PostgresConnector() as db:
        db.execute_insert("INSERT INTO task_run (task_name, start_date, end_date, status, additional_info) VALUES (%s, %s, now(), %s, %s)", [task_name, start_time, status, additional_info])

def get_task_config(task_name, config_name):
    with PostgresConnector() as db:
        result = db.execute_select("SELECT config_value FROM task_config WHERE task_name = %s AND config_name = %s", [task_name, config_name], fetch_one=True)
    
    if result:
        return result[0]