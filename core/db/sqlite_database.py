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

    def execute_file(self, filepath):
        with open(filepath, 'r') as f:
            sql = f.read()
        self.cursor.execute(sql)
        self.conn.commit()
   
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()