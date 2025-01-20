import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query, params=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        result = cursor.fetchall()
        conn.close()
        return result