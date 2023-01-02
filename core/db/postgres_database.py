import os
import psycopg2

class PostgresConnector:
    def __init__(self):
        self.host = os.environ['POSTGRES_HOST']
        self.database = os.environ['POSTGRES_DATABASE']
        self.user = os.environ['POSTGRES_USER']
        self.password = os.environ['POSTGRES_PASSWORD']
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        with self.conn.cursor() as cursor:
            cursor.execute("SET search_path TO cerebro")
            
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def execute_select(self, query, params=None, fetch_one=False):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()

    def execute_insert(self, query, params=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.conn.commit()

    def execute_update(self, query, params=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.conn.commit()
    
    def execute_file(self, filepath):
        with open(filepath, 'r') as f:
            sql = f.read()
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            self.conn.commit()