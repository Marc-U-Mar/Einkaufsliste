import tkinter as tk
from tkinter import ttk

class PurchasedListView:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.purchased_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.purchased_listbox.pack(side="left", fill="both", expand=True)
        self.purchased_listbox.bind('<Double-1>', self.on_double_click)

        purchased_items_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.purchased_listbox.yview)
        purchased_items_scrollbar.pack(side="right", fill="y")
        self.purchased_listbox.config(yscrollcommand=purchased_items_scrollbar.set)

        ttk.Label(master, text="Bisher eingekaufte Artikel:").grid(row=9, column=0, sticky="w", padx=5, pady=5)

    def update_list(self, items):
        self.purchased_listbox.delete(0, tk.END)
        for item in items:
            self.purchased_listbox.insert(tk.END, item)

    def get_selected_item(self):
        selected = self.purchased_listbox.curselection()
        if selected:
            return self.purchased_listbox.get(selected)
        return None

    def on_double_click(self, event):
        if self.double_click_handler:
            selected_item = self.get_selected_item()
            if selected_item:
                self.double_click_handler(selected_item)

    def set_double_click_handler(self, handler):
        self.double_click_handler = handler