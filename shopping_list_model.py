from tkinter import filedialog as fd
from datetime import datetime, date

class ShoppingListModel:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db_manager.create_database()

    def get_shopping_list(self):
        return self.db_manager.execute_query('SELECT product_name, typical_duration, price FROM current_shopping_list')

    def get_formatted_shopping_list(self):
        items = self.get_shopping_list()
        formatted_items = []
        total_budget = 0
        for item in items:
            formatted_items.append(f"{item[0]} (Verbrauchsdauer: {item[1]} Tage, {item[2]:.2f} €)")
            total_budget += item[2]
        formatted_items.append(f"Gesamtkosten: {total_budget:.2f} €")
        return formatted_items

    def add_product(self, name, duration, price):
        result = self.db_manager.execute_query('SELECT * FROM current_shopping_list WHERE product_name = ?', (name,))
# Verhindert Duplikate in der Einkaufsliste
        if not result:
            self.db_manager.execute_query(
                'INSERT INTO current_shopping_list (product_name, typical_duration, price) VALUES (?, ?, ?)',
                (name, duration, price))
            return True
        return False

    def delete_product(self, product_name):
        self.db_manager.execute_query('DELETE FROM current_shopping_list WHERE product_name = ?', (product_name,))

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

    def export_shopping_list(self, purchase_date):
        items = self.get_shopping_list()
        if not items:
            return None, "Keine Artikel in der Einkaufsliste."

        export_content = f"Einkaufsliste - Exportiert am: {datetime.now().strftime('%Y-%m-%d')}\n"
        export_content += f"Geplantes Einkaufsdatum: {purchase_date}\n\n"
        total_cost = 0
        for item in items:
            product_name, typical_duration, price = item
            export_content += f"{product_name} (Verbrauchsdauer: {typical_duration} Tage, Preis: {price:.2f} €)\n"
            total_cost += price
        export_content += f"\nGesamtkosten: {total_cost:.2f} €"

        default_filename = f"Einkaufsliste_{datetime.now().strftime('%Y-%m-%d')}.txt"

        file_path = fd.asksaveasfilename(
            title="Einkaufsliste speichern",
            defaultextension=".txt",
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")],
            initialfile=default_filename
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(export_content)

            for item in items:
                product_name, typical_duration, price = item
                self.db_manager.execute_query(
                    'INSERT OR REPLACE INTO shopping_list (product_name, typical_duration, last_purchase_date, price) VALUES (?, ?, ?, ?)',
                    (product_name, typical_duration, purchase_date, price)
                )

            self.db_manager.execute_query('DELETE FROM current_shopping_list')

            return file_path, export_content

        return None, None

    def check_and_update_database(self):
        columns = self.db_manager.execute_query("PRAGMA table_info(current_shopping_list)")
        if 'typical_duration' not in [column[1] for column in columns]:
            self.db_manager.execute_query("ALTER TABLE current_shopping_list ADD COLUMN typical_duration INTEGER")

    def check_and_update_item(self, product_name, typical_duration, purchase_date, price):
        self.db_manager.execute_query(
            'INSERT OR REPLACE INTO shopping_list (product_name, typical_duration, last_purchase_date, price) VALUES (?, ?, ?, ?)',
            (product_name, typical_duration, purchase_date, price))

    def add_purchased_item(self, name, duration, date, price):
        self.db_manager.execute_query(
            'INSERT OR REPLACE INTO shopping_list (product_name, typical_duration, last_purchase_date, price) VALUES (?, ?, ?, ?)',
            (name, duration, date, price))

    def reset_expired_items(self):
        today = date.today()
        purchased_items = self.db_manager.execute_query(
            'SELECT product_name, typical_duration, last_purchase_date, price FROM shopping_list')

        for item in purchased_items:
            product_name, typical_duration, last_purchase_date, price = item
            last_purchase = datetime.strptime(last_purchase_date, "%Y-%m-%d").date()
            days_since_purchase = (today - last_purchase).days

# Automatisiert die Erstellunge der Einkaufliste basierend auf typischen Verbrauchsdauer der Produkte
            if days_since_purchase > typical_duration:
                existing = self.db_manager.execute_query(
                    'SELECT * FROM current_shopping_list WHERE product_name = ?', (product_name,))

                if not existing:
                    self.db_manager.execute_query(
                        'INSERT INTO current_shopping_list (product_name, typical_duration, price) VALUES (?, ?, ?)',
                        (product_name, typical_duration, price))

    @staticmethod
    def create_export_content(items, purchase_date):
        content = f"Einkaufsdatum: {purchase_date}\n\n"
        for item in items:
            content += f"{item[0]} (Verbrauchsdauer: {item[1]} Tage, Preis: {item[2]:.2f} €)\n"
        content += f"\nGesamtkosten: {sum(item[2] for item in items):.2f} €"
        return content

    @staticmethod
    def validate_date(date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def calculate_total_budget(items):
        return sum(item[2] for item in items)
