import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import sqlite3
from datetime import datetime
from product import Product
from inventory import Inventory
from shopping_list_generator import ShoppingListGenerator
from shopping_list_manager import ShoppingListManager


class ShoppingListGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Einkaufslisten-Generator")
        self.manager = ShoppingListManager()
        self.inventory = Inventory()
        self.shopping_list_generator = ShoppingListGenerator()

        self.create_widgets()
        self.update_shopping_list_on_startup()
        self.display_purchased_items()
        self.display_shopping_list()


    def create_widgets(self):
        ttk.Label(self.master, text="Produktname:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.product_name = ttk.Entry(self.master)
        self.product_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Verbrauchsdauer (Tage):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.typical_duration = ttk.Entry(self.master)
        self.typical_duration.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Preis:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.price = ttk.Entry(self.master)
        self.price.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.master, text="Produkt hinzufügen", command=self.add_product).grid(row=3, column=0, columnspan=2,
                                                                                          pady=10)

        ttk.Label(self.master, text="Einkaufsliste:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        shopping_list_frame = ttk.Frame(self.master)
        shopping_list_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.shopping_list = tk.Listbox(shopping_list_frame, width=50, height=10)
        self.shopping_list.pack(side="left", fill="both", expand=True)
        shopping_list_scrollbar = ttk.Scrollbar(shopping_list_frame, orient="vertical", command=self.shopping_list.yview)
        shopping_list_scrollbar.pack(side="right", fill="y")
        self.shopping_list.config(yscrollcommand=shopping_list_scrollbar.set)

        ttk.Button(self.master, text="Einkaufsliste aktualisieren", command=self.display_shopping_list).grid(row=6,
                                                                                                             column=0,
                                                                                                             columnspan=2,
                                                                                                             pady=10)

        ttk.Button(self.master, text="Produkt löschen", command=self.delete_selected_product).grid(row=7, column=0,
                                                                                                   columnspan=2,
                                                                                                   pady=10)

        ttk.Button(self.master, text="Einkaufsliste exportieren", command=self.export_shopping_list).grid(row=8,
                                                                                                          column=0,
                                                                                                          columnspan=2,
                                                                                                          pady=10)

        ttk.Label(self.master, text="Bisher eingekaufte Artikel:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        purchased_items_frame = ttk.Frame(self.master)
        purchased_items_frame.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.purchased_listbox = tk.Listbox(purchased_items_frame, width=50, height=10)
        self.purchased_listbox.pack(side="left", fill="both", expand=True)
        purchased_items_scrollbar = ttk.Scrollbar(purchased_items_frame, orient="vertical", command=self.purchased_listbox.yview)
        purchased_items_scrollbar.pack(side="right", fill="y")
        self.purchased_listbox.config(yscrollcommand=purchased_items_scrollbar.set)
        self.purchased_listbox.bind('<Double-1>', self.add_to_shopping_list)

        self.status_label = ttk.Label(self.master, text="")
        self.status_label.grid(row=11, column=0, columnspan=2, pady=5)

    def update_shopping_list_on_startup(self):
        self.manager.update_shopping_list_on_startup()
        self.display_shopping_list()

    def add_product(self):
        name = self.product_name.get()
        duration = self.typical_duration.get()
        price = self.price.get()

        if not name or not duration or not price:
            self.show_status("Bitte füllen Sie alle Felder aus.")
            return

        try:
            duration = int(duration)
            price = float(price)
        except ValueError:
            self.show_status("Ungültige Eingabe für Verbrauchsdauer oder Preis.")
            return

        if self.manager.add_product(name, duration, price):
            self.show_status(f"'{name}' wurde zur Einkaufsliste hinzugefügt.")
        else:
            self.show_status(f"'{name}' ist bereits auf der Einkaufsliste.")

        self.product_name.delete(0, tk.END)
        self.typical_duration.delete(0, tk.END)
        self.price.delete(0, tk.END)

        self.display_shopping_list()

    def display_shopping_list(self):
        self.shopping_list.delete(0, tk.END)
        items = self.manager.get_shopping_list()

        total_budget = self.manager.calculate_total_budget(items)
        for item in items:
            self.shopping_list.insert(tk.END, f"{item[0]} (Verbrauchsdauer: {item[1]} Tage, {item[2]:.2f} €)")

        self.shopping_list.insert(tk.END, f"Gesamtkosten: {total_budget:.2f} €")

    def display_purchased_items(self):
        items = self.manager.get_purchased_items()

        self.purchased_listbox.delete(0, tk.END)
        for item in items:
            display_text = self.manager.format_purchased_item(item)
            self.purchased_listbox.insert(tk.END, display_text)

        self.show_status("Liste der gekauften Artikel wurde aktualisiert.")

    def delete_selected_product(self):
        selected_shopping = self.shopping_list.curselection()
        selected_purchased = self.purchased_listbox.curselection()

        if selected_shopping:
            product_text = self.shopping_list.get(selected_shopping)
            product_name = product_text.split(" (")[0]
            self.manager.delete_from_current_shopping_list(product_name)
            self.show_status(f"Das Produkt '{product_name}' wurde von der Einkaufsliste entfernt.")
        elif selected_purchased:
            product_text = self.purchased_listbox.get(selected_purchased)
            product_name = product_text.split(" (")[0]
            self.manager.delete_from_purchased_list(product_name)
            self.show_status(f"Das Produkt '{product_name}' wurde aus der Liste 'Bisher gekaufte Artikel' entfernt.")
        else:
            self.show_status("Bitte wählen Sie ein Produkt aus, das gelöscht werden soll.")
            return

        self.display_shopping_list()
        self.display_purchased_items()

    def delete_from_current_shopping_list(self, product_name):
        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM current_shopping_list WHERE product_name = ?', (product_name,))
        conn.commit()
        conn.close()
        self.show_status(f"Das Produkt '{product_name}' wurde von der Einkaufsliste entfernt.")

    def delete_from_purchased_list(self, product_name):
        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shopping_list WHERE product_name = ?', (product_name,))
        conn.commit()
        conn.close()
        self.show_status(f"Das Produkt '{product_name}' wurde aus der Liste 'Bisher gekaufte Artikel' entfernt.")

    def add_to_shopping_list(self, event):
        selected = self.purchased_listbox.curselection()
        if not selected:
            return

        product_text = self.purchased_listbox.get(selected)
        product_name = product_text.split(" (")[0]

        result = self.manager.add_to_shopping_list(product_name)
        if result is True:
            self.show_status(f"'{product_name}' wurde zur Einkaufsliste hinzugefügt.")
        elif result is False:
            self.show_status(f"'{product_name}' ist bereits auf der Einkaufsliste.")
        else:
            self.show_status(f"Fehler: Keine Verbrauchsdauer für '{product_name}' gefunden.")

        self.display_shopping_list()

    def show_status(self, message):
        self.status_label.config(text=message)
        self.master.after(3000, lambda: self.status_label.config(text=""))

    def get_purchase_date(self):
        purchase_date = simpledialog.askstring("Einkaufsdatum", "Bitte geben Sie das Einkaufsdatum ein (YYYY-MM-DD):")
        return purchase_date

    def export_shopping_list(self):
        purchase_date = self.get_purchase_date()
        if not purchase_date:
            self.show_status("Export abgebrochen.")
            return

        items = self.manager.export_shopping_list(purchase_date)

        self.display_shopping_list()
        self.display_purchased_items()

        current_date = datetime.now().strftime("%Y-%m-%d")
        default_filename = f"Einkaufsliste_{current_date}.txt"
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"Einkaufsdatum: {purchase_date}\n\n")
                for item in items:
                    file.write(f"{item[0]} (Verbrauchsdauer: {item[1]} Tage, Preis: {item[2]:.2f} €)\n")
                file.write(f"\nGesamtkosten: {sum(item[2] for item in items):.2f} €")
            self.show_status(f"Einkaufsliste wurde exportiert und Artikel wurden aktualisiert.")