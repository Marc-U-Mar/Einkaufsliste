import tkinter as tk
from tkinter import ttk

class ShoppingListView:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.shopping_list = tk.Listbox(self.frame, width=50, height=10)
        self.shopping_list.pack(side="left", fill="both", expand=True)

        shopping_list_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.shopping_list.yview)
        shopping_list_scrollbar.pack(side="right", fill="y")
        self.shopping_list.config(yscrollcommand=shopping_list_scrollbar.set)

        ttk.Label(master, text="Einkaufsliste:").grid(row=4, column=0, sticky="w", padx=5, pady=5)

    def update_list(self, items):
        self.shopping_list.delete(0, tk.END)
        for item in items:
            self.shopping_list.insert(tk.END, item)

    def get_selected_item(self):
        selected = self.shopping_list.curselection()
        if selected:
            return self.shopping_list.get(selected)
        return None
