import tkinter as tk
from shopping_list_gui import ShoppingListGUI
from shopping_list_manager import ShoppingListManager
from shopping_list_generator import ShoppingListGenerator

class ShoppingListApp:
    def __init__(self):
        self.root = tk.Tk()
        manager = ShoppingListManager()
        generator = ShoppingListGenerator()
        self.gui = ShoppingListGUI(self.root, manager, generator)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ShoppingListApp()
    app.run()
