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

def get_task_status(task_name):
    with PostgresConnector() as db:
        result = db.execute_select("SELECT status FROM task WHERE name = %s", [task_name], fetch_one=True)
    
    if result:
        return result[0]

def check_if_now_matches_expr(now, expression):
    def cron_schedule_expr_to_list(expression):
        def expr_to_list(expr, start_range, end_range):
            if expr == '*':
                return list(range(start_range, end_range))
            elif '/' in expr:
                start, step = expr.split('/')
                if start != '*':
                    start_range = int(start)

                step = int(step)
                return list(range(start_range, end_range, step))
            else:
                return [int(expr)]

        minute, hour, day, month, wday = expression.split(' ')
        day =  expr_to_list(day, 1, 32)
        minute = expr_to_list(minute, 0, 60)
        hour = expr_to_list(hour, 0, 24)
        month = expr_to_list(month, 1, 13)
        wday = expr_to_list(wday, 0, 7)
        
        return minute, hour, day, month, wday 
        
    minute, hour, day, month, wday = cron_schedule_expr_to_list(expression)
    if now.month in month:
        if now.day in day and now.weekday() in wday:
            if now.hour in hour:
                if now.minute in minute:
                    return True
    return False