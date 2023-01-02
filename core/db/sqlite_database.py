import sqlite3

class SQLiteDatabase:
    def __init__(self, db_file='assets/cerebro.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.conn.commit()

    def execute_fetchone(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def execute_fetchall(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    def create_tables(self):
        queries = []
        queries.append('''CREATE TABLE IF NOT EXISTS asn_data (id INTEGER PRIMARY KEY, country_code TEXT, ip_range_start TEXT, ip_range_end TEXT, create_date TEXT, last_seen_date TEXT, last_scan_date TEXT)''')
        queries.append('''CREATE TABLE IF NOT EXISTS ip (id INTEGER PRIMARY KEY AUTOINCREMENT, asn_data_id INT, ipv4 TEXT, ipv6 TEXT, hostname TEXT, status TEXT)''')
        queries.append('''CREATE TABLE IF NOT EXISTS task (name TEXT PRIMARY KEY, frequency TEXT, last_run_date TEXT, status TEXT)''')
        queries.append('''CREATE TABLE IF NOT EXISTS task_run (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, start_date TEXT, end_date TEXT, status TEXT, additional_info TEXT)''')
        queries.append('''CREATE TABLE IF NOT EXISTS task_config (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, config_name TEXT, config_value TEXT)''')
        queries.append('''CREATE TABLE IF NOT EXISTS event (id INTEGER PRIMARY KEY AUTOINCREMENT, event_name TEXT, timestamp TEXT, message TEXT, type TEXT)''')

        for query in queries:
            self.execute(query)
        self.conn.commit()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()