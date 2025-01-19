import sqlite3

class ShoppingListManager:
    def __init__(self, db_name='shopping_list.db'):
        self.db_name = db_name
        self.create_database()
        self.check_and_update_database()

    def create_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                typical_duration INTEGER NOT NULL,
                last_purchase_date TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS current_shopping_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                typical_duration INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def check_and_update_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(current_shopping_list)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'typical_duration' not in columns:
            cursor.execute("ALTER TABLE current_shopping_list ADD COLUMN typical_duration INTEGER")
            conn.commit()
        conn.close()

    def add_product(self, name, duration, price):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM current_shopping_list WHERE product_name = ?', (name,))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO current_shopping_list (product_name, typical_duration, price) VALUES (?, ?, ?)',
                           (name, duration, price))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    def get_shopping_list(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT product_name, typical_duration, price FROM current_shopping_list')
        items = cursor.fetchall()
        conn.close()
        return items

    def calculate_total_budget(self, items):
        return sum(item[2] for item in items)

    def get_purchased_items(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT product_name, typical_duration, last_purchase_date, price FROM shopping_list')
        items = cursor.fetchall()
        conn.close()
        return items

    def format_purchased_item(self, item):
        product_name = item[0] if len(item) > 0 else "Unbekannt"
        last_purchase = item[2] if len(item) > 2 else "Unbekannt"
        price = item[3] if len(item) > 3 else 0.0

        display_text = f"{product_name} (Letzter Kauf: {last_purchase}"
        if isinstance(price, (int, float)):
            display_text += f", Preis: {price:.2f} €)"
        else:
            display_text += ")"

        return display_text

    def delete_from_current_shopping_list(self, product_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM current_shopping_list WHERE product_name = ?', (product_name,))
        conn.commit()
        conn.close()

    def delete_from_purchased_list(self, product_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shopping_list WHERE product_name = ?', (product_name,))
        conn.commit()
        conn.close()

    def add_to_shopping_list(self, product_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT typical_duration, price FROM shopping_list WHERE product_name = ?', (product_name,))
        result = cursor.fetchone()
        if result:
            typical_duration, price = result
            cursor.execute('SELECT * FROM current_shopping_list WHERE product_name = ?', (product_name,))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO current_shopping_list (product_name, typical_duration, price) 
                    VALUES (?, ?, ?)
                ''', (product_name, typical_duration, price or 0.0))
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                return False
        else:
            conn.close()
            return None

    def export_shopping_list(self, purchase_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT product_name, typical_duration, price FROM current_shopping_list')
        items = cursor.fetchall()
        for item in items:
            product_name, typical_duration, price = item
            self.check_and_update_item(product_name, typical_duration, purchase_date, price)
        cursor.execute('DELETE FROM current_shopping_list')
        conn.commit()
        conn.close()
        return items

    def check_and_update_item(self, product_name, typical_duration, purchase_date, price):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM shopping_list WHERE product_name = ?', (product_name,))
        existing_item = cursor.fetchone()
        if existing_item:
            cursor.execute('UPDATE shopping_list SET last_purchase_date = ? WHERE product_name = ?',
                           (purchase_date, product_name))
        else:
            cursor.execute(
                'INSERT INTO shopping_list (product_name, typical_duration, last_purchase_date, price) VALUES (?, ?, ?, ?)',
                (product_name, typical_duration, purchase_date, price))
        conn.commit()
        conn.close()

    def update_shopping_list_on_startup(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT product_name, typical_duration, price FROM shopping_list')
        items = cursor.fetchall()
        for item in items:
            product_name, typical_duration, price = item
            cursor.execute('SELECT * FROM current_shopping_list WHERE product_name = ?', (product_name,))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO current_shopping_list (product_name, typical_duration, price)
                    VALUES (?, ?, ?)
                ''', (product_name, typical_duration, price or 0.0))
        conn.commit()
        conn.close()