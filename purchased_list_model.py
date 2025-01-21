class PurchasedListModel:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_purchased_items(self):
        return self.db_manager.execute_query('SELECT product_name, typical_duration, last_purchase_date, price FROM shopping_list')

    def get_formatted_purchased_items(self):
        items = self.get_purchased_items()
        return [self.format_purchased_item(item) for item in items]

    def delete_purchased_item(self, product_name):
        self.db_manager.execute_query('DELETE FROM shopping_list WHERE product_name = ?', (product_name,))

    def add_purchased_item(self, name, duration, date, price):
        self.db_manager.execute_query(
            'INSERT OR REPLACE INTO shopping_list (product_name, typical_duration, last_purchase_date, price) VALUES (?, ?, ?, ?)',
            (name, duration, date, price)
        )

    def remove_older_duplicates(self):
        self.db_manager.execute_query('''
            DELETE FROM shopping_list
            WHERE rowid NOT IN (
                SELECT MAX(rowid)
                FROM shopping_list
                GROUP BY product_name
            )
        ''')

    def add_to_shopping_list(self, product_name):
        result = self.db_manager.execute_query('SELECT typical_duration, price FROM shopping_list WHERE product_name = ?', (product_name,))
        if result:
            typical_duration, price = result[0]
            existing = self.db_manager.execute_query('SELECT * FROM current_shopping_list WHERE product_name = ?', (product_name,))
            if not existing:
                self.db_manager.execute_query('''
                    INSERT INTO current_shopping_list (product_name, typical_duration, price)
                    VALUES (?, ?, ?)
                ''', (product_name, typical_duration, price or 0.0))
                return True
            return False
        return None

    @staticmethod
    def format_purchased_item(item):
        product_name = item[0] if len(item) > 0 else "Unbekannt"
        last_purchase = item[2] if len(item) > 2 else "Unbekannt"
        price = item[3] if len(item) > 3 else 0.0
        display_text = f"{product_name} (Letzter Kauf: {last_purchase}"
        if isinstance(price, (int, float)):
            display_text += f", Preis: {price:.2f} €)"
        else:
            display_text += ")"
        return display_text
