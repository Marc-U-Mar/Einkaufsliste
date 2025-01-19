import sqlite3
from datetime import datetime, timedelta

class ShoppingListGenerator:
    def __init__(self, db_name='shopping_list.db'):
        self.db_name = db_name

    def generate_shopping_list(self, current_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT product_name, typical_duration, last_purchase_date
            FROM shopping_list
        ''')
        items = cursor.fetchall()
        conn.close()

        shopping_list = []
        current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")

        for item in items:
            product_name, typical_duration, last_purchase_date = item
            if last_purchase_date:
                try:
                    last_purchase_date_obj = datetime.strptime(last_purchase_date, "%Y-%m-%d")
                    next_purchase_date = last_purchase_date_obj + timedelta(days=typical_duration)

                    if next_purchase_date <= current_date_obj:
                        shopping_list.append(product_name)
                except ValueError:
                    shopping_list.append(product_name)
            else:
                shopping_list.append(product_name)

        return shopping_list
