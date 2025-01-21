import tkinter as tk
from shopping_list_model import ShoppingListModel
from purchased_list_model import PurchasedListModel
from shopping_list_view import ShoppingListView
from purchased_list_view import PurchasedListView
from input_view import InputView
from shopping_list_controller import ShoppingListController
from purchased_list_controller import PurchasedListController
from input_controller import InputController
from database_manager import DatabaseManager
from gui_manager import GUIManager

class ShoppingListApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Einkaufslisten-Generator")

        # Initialisierung des Datenbankmanagers
        self.db_manager = DatabaseManager('shopping_list.db')
        self.db_manager.create_database()

        # Modelle erstellen
        self.shopping_list_model = ShoppingListModel(self.db_manager)
        self.purchased_list_model = PurchasedListModel(self.db_manager)

        # Entfernen älterer Duplikate beim Start der App
        self.purchased_list_model.remove_older_duplicates()

        # Views erstellen
        shopping_list_view = ShoppingListView(self.root)
        purchased_list_view = PurchasedListView(self.root)
        input_view = InputView(self.root)

        # Controller erstellen und verbinden
        self.shopping_list_controller = ShoppingListController(self.shopping_list_model, shopping_list_view)
        self.purchased_list_controller = PurchasedListController(
            self.purchased_list_model,
            purchased_list_view,
            self.shopping_list_controller
        )
        self.input_controller = InputController(input_view, self.shopping_list_controller)

        # Setzen des PurchasedListControllers für den ShoppingListController
        self.shopping_list_controller.set_purchased_list_controller(self.purchased_list_controller)

        # Automatische Überprüfung und Aktualisierung bei jedem Appstart
        self.shopping_list_model.reset_expired_items()

        # GUI-Manager einrichten
        self.gui_manager = GUIManager(self.root, self.shopping_list_controller,
                                      self.purchased_list_controller, self.input_controller)
        self.gui_manager.setup_gui()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ShoppingListApp()
    app.run()
