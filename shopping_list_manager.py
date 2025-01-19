import sqlite3
from datetime import datetime


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

    def validate_date(self, date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

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

        # Erstellen des formatierten Inhalts
        content = f"Einkaufsdatum: {purchase_date}\n\n"
        total_cost = 0
        for item in items:
            content += f"{item[0]} (Verbrauchsdauer: {item[1]} Tage, Preis: {item[2]:.2f} €)\n"
            total_cost += item[2]
        content += f"\nGesamtkosten: {total_cost:.2f} €"

        return items, content

    def create_export_content(self, items, purchase_date):
        content = f"Einkaufsdatum: {purchase_date}\n\n"
        for item in items:
            content += f"{item[0]} (Verbrauchsdauer: {item[1]} Tage, Preis: {item[2]:.2f} €)\n"
        content += f"\nGesamtkosten: {sum(item[2] for item in items):.2f} €"
        return content

    def delete_product(self, product_name, is_shopping_list):
        if is_shopping_list:
            self.delete_from_current_shopping_list(product_name)
            return f"Das Produkt '{product_name}' wurde von der Einkaufsliste entfernt."
        else:
            self.delete_from_purchased_list(product_name)
            return f"Das Produkt '{product_name}' wurde aus der Liste 'Bisher gekaufte Artikel' entfernt."

    def get_formatted_shopping_list(self):
        items = self.get_shopping_list()
        formatted_items = []
        total_budget = 0
        for item in items:
            formatted_items.append(f"{item[0]} (Verbrauchsdauer: {item[1]} Tage, {item[2]:.2f} €)")
            total_budget += item[2]
        formatted_items.append(f"Gesamtkosten: {total_budget:.2f} €")
        return formatted_items

    def get_formatted_purchased_items(self):
        items = self.get_purchased_items()
        formatted_items = []
        for item in items:
            product_name = item[0] if len(item) > 0 else "Unbekannt"
            last_purchase = item[2] if len(item) > 2 else "Unbekannt"
            price = item[3] if len(item) > 3 else 0.0

            display_text = f"{product_name} (Letzter Kauf: {last_purchase}"
            if isinstance(price, (int, float)):
                display_text += f", Preis: {price:.2f} €)"
            else:
                display_text += ")"

            formatted_items.append(display_text)

        return formatted_items

    def validate_and_add_product(self, name, duration, price):
        if not name or not duration or not price:
            return False, "Bitte füllen Sie alle Felder aus."

        try:
            duration = int(duration)
            price = float(price)
        except ValueError:
            return False, "Ungültige Eingabe für Verbrauchsdauer oder Preis."

        if self.add_product(name, duration, price):
            return True, f"'{name}' wurde zur Einkaufsliste hinzugefügt."
        else:
            return False, f"'{name}' ist bereits auf der Einkaufsliste."

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