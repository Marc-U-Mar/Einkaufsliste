from datetime import datetime
from tkinter import simpledialog

class ShoppingListController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.purchased_list_controller = None

    def get_purchase_date(self):
        today = datetime.now().strftime("%Y-%m-%d")
        date_string = simpledialog.askstring("Einkaufsdatum",
                                             "Bitte geben Sie das Einkaufsdatum ein (YYYY-MM-DD):",
                                             initialvalue=today)
        if date_string and self.validate_date(date_string):
            return date_string
        return None

# Ermöglicht die Kommunikation zwischen den Controllern für das Hinzufügen von Artikeln auf die Einkaufliste
    def set_purchased_list_controller(self, purchased_list_controller):
        self.purchased_list_controller = purchased_list_controller

    def check_and_reset_expired_items(self):
        self.model.reset_expired_items()
        self.update_shopping_list()

    @staticmethod
    def validate_date(date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_product(self, name, duration, price):
        success, message = self.model.validate_and_add_product(name, duration, price)
        if success:
            self.update_shopping_list()
        return message

    def delete_product(self, product_name):
        self.model.delete_product(product_name)
        self.update_shopping_list()

    def update_purchased_list(self):
        items = self.model.get_formatted_purchased_items()
        self.view.update_list(items)

    def update_shopping_list(self):
        items = self.model.get_formatted_shopping_list()
        self.view.update_list(items)

    def export_shopping_list(self):
        purchase_date = self.get_purchase_date()
        if purchase_date:
            file_path, export_content = self.model.export_shopping_list(purchase_date)
            if file_path:
                self.update_shopping_list()
                self.purchased_list_controller.update_purchased_list()
                return file_path, export_content
        return None, None

    @staticmethod
    def validate_date(date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
