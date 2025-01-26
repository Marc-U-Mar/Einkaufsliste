import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_database(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS shopping_list (
                product_name TEXT PRIMARY KEY,
                typical_duration INTEGER,
                last_purchase_date TEXT,
                price REAL
            )
        ''')
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS current_shopping_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                typical_duration INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')

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