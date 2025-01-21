import tkinter as tk

class GUIManager:
    def __init__(self, root, shopping_list_controller, purchased_list_controller, input_controller):
        self.root = root
        self.shopping_list_controller = shopping_list_controller
        self.purchased_list_controller = purchased_list_controller
        self.input_controller = input_controller

    def setup_gui(self):
        tk.Button(self.root, text="Produkt hinzufügen",
                  command=self.input_controller.add_product).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Einkaufsliste aktualisieren",
                  command=self.shopping_list_controller.update_shopping_list).grid(row=6, column=0, columnspan=2,
                                                                                   pady=10)

        tk.Button(self.root, text="Produkt löschen",
                  command=self.delete_selected_product).grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Einkaufsliste exportieren",
                  command=self.shopping_list_controller.export_shopping_list).grid(row=8, column=0, columnspan=2,
                                                                                   pady=10)

        self.shopping_list_controller.update_shopping_list()
        self.purchased_list_controller.update_purchased_list()

    def delete_selected_product(self):
        selected_shopping = self.shopping_list_controller.view.get_selected_item()
        selected_purchased = self.purchased_list_controller.view.get_selected_item()

        if selected_shopping:
            product_name = selected_shopping.split(" (")[0]  # Extrahiert den Produktnamen
            self.shopping_list_controller.delete_product(product_name)
            self.shopping_list_controller.update_shopping_list()
        elif selected_purchased:
            product_name = selected_purchased.split(" (")[0]  # Extrahiert den Produktnamen
            self.purchased_list_controller.delete_product(product_name)
            self.purchased_list_controller.update_purchased_list()

    def export_shopping_list(self):
        file_path = self.shopping_list_controller.export_shopping_list()
        if file_path:
            print(f"Einkaufsliste erfolgreich exportiert. Datei gespeichert unter: {file_path}")
        else:
            print("Export fehlgeschlagen oder abgebrochen.")

