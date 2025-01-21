class PurchasedListController:
    def __init__(self, model, view, shopping_list_controller):
        self.model = model
        self.view = view
        self.shopping_list_controller = shopping_list_controller

        self.view.set_double_click_handler(self.add_to_shopping_list)

    def delete_product(self, product_name):
        self.model.delete_purchased_item(product_name)
        self.update_purchased_list()

    def update_purchased_list(self):
        items = self.model.get_formatted_purchased_items()
        self.view.update_list(items)

    def add_to_shopping_list(self, item):
        product_name = item.split(" (")[0]
        result = self.model.add_to_shopping_list(product_name)
        if result is True:
            self.shopping_list_controller.update_shopping_list()
            return f"'{product_name}' wurde zur Einkaufsliste hinzugefügt."
        elif result is False:
            return f"'{product_name}' ist bereits auf der Einkaufsliste."
        else:
            return f"Fehler: Keine Verbrauchsdauer für '{product_name}' gefunden."