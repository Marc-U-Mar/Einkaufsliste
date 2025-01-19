import tkinter as tk
from shopping_list_gui import ShoppingListGUI

class ShoppingListApp:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = ShoppingListGUI(self.root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ShoppingListApp()
    app.run()
