import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import sqlite3
from datetime import datetime
from product import Product
from inventory import Inventory
from shopping_list_generator import ShoppingListGenerator


class ShoppingListGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Einkaufslisten-Generator")
        self.inventory = Inventory()
        self.shopping_list_generator = ShoppingListGenerator()

        self.create_database()
        self.check_and_update_database()
        self.create_widgets()
        self.update_shopping_list_on_startup()
        self.display_purchased_items()
        self.display_shopping_list()

    def create_database(self):
        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                typical_duration INTEGER NOT NULL,
                last_purchase_date TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS current_shopping_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                typical_duration INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def check_and_update_database(self):
        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(current_shopping_list)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'typical_duration' not in columns:
            cursor.execute("ALTER TABLE current_shopping_list ADD COLUMN typical_duration INTEGER")
            conn.commit()
            print("Spalte 'typical_duration' wurde zur Tabelle 'current_shopping_list' hinzugefügt.")

        conn.close()

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

        self.status_label = ttk.Label(self.master, text="")
        self.status_label.grid(row=11, column=0, columnspan=2, pady=5)

    def update_shopping_list_on_startup(self):
        current_date = datetime.now()
        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()

        cursor.execute('SELECT product_name, typical_duration, last_purchase_date FROM shopping_list')
        items = cursor.fetchall()

        for item in items:
            product_name, typical_duration, last_purchase_date = item
            last_purchase_date_obj = datetime.strptime(last_purchase_date, '%Y-%m-%d')
            days_since_purchase = (current_date - last_purchase_date_obj).days
            if days_since_purchase >= typical_duration:
                cursor.execute('SELECT * FROM current_shopping_list WHERE product_name = ?', (product_name,))
                if cursor.fetchone() is None:
                    cursor.execute('''
                        INSERT INTO current_shopping_list (product_name, typical_duration)
                        VALUES (?, ?)
                    ''', (product_name, typical_duration))

        conn.commit()
        conn.close()

    def add_product(self):
        name = self.product_name.get()
        duration = int(self.typical_duration.get())
        price = float(self.price.get())

        if not price:
            self.show_status("Bitte geben Sie einen Preis ein.")
            return

        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM current_shopping_list WHERE product_name = ?', (name,))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO current_shopping_list (product_name, typical_duration, price) VALUES (?, ?, ?)',
                           (name, duration, price))
            conn.commit()
            self.show_status(f"'{name}' wurde zur Einkaufsliste hinzugefügt.")
        else:
            self.show_status(f"'{name}' ist bereits auf der Einkaufsliste.")

        conn.close()

        self.product_name.delete(0, tk.END)
        self.typical_duration.delete(0, tk.END)
        self.price.delete(0, tk.END)

        self.display_shopping_list()

    def display_shopping_list(self):
        self.shopping_list.delete(0, tk.END)
        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()
        cursor.execute('SELECT product_name, typical_duration, price FROM current_shopping_list')
        items = cursor.fetchall()
        conn.close()

        total_budget = 0
        for item in items:
            self.shopping_list.insert(tk.END, f"{item[0]} (Verbrauchsdauer: {item[1]} Tage, {item[2]:.2f} €)")
            total_budget += item[2]

        self.shopping_list.insert(tk.END, f"Gesamtkosten: {total_budget:.2f} €")

    def display_purchased_items(self):
        items = self.get_purchased_items()

        self.purchased_listbox.delete(0, tk.END)
        for item in items:
            self.purchased_listbox.insert(tk.END, f"{item[0]} (Letzter Kauf: {item[2]}, Preis: {item[3]:.2f} €)")

    def get_purchased_items(self):
        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()
        cursor.execute('SELECT product_name, typical_duration, last_purchase_date FROM shopping_list')
        items = cursor.fetchall()
        conn.close()
        return items

    def delete_selected_product(self):
        selected_shopping = self.shopping_list.curselection()
        selected_purchased = self.purchased_listbox.curselection()

        if selected_shopping:
            product_text = self.shopping_list.get(selected_shopping)
            product_name = product_text.split(" (")[0]
            self.delete_from_current_shopping_list(product_name)
        elif selected_purchased:
            product_text = self.purchased_listbox.get(selected_purchased)
            product_name = product_text.split(" (")[0]
            self.delete_from_purchased_list(product_name)
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

        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()

        cursor.execute('SELECT typical_duration FROM shopping_list WHERE product_name = ?', (product_name,))
        result = cursor.fetchone()
        if result:
            typical_duration = result[0]
            cursor.execute('SELECT * FROM current_shopping_list WHERE product_name = ?', (product_name,))
            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO current_shopping_list (product_name, typical_duration) VALUES (?, ?)',
                               (product_name, typical_duration))
                conn.commit()
                self.show_status(f"'{product_name}' wurde zur Einkaufsliste hinzugefügt.")
            else:
                self.show_status(f"'{product_name}' ist bereits auf der Einkaufsliste.")
        else:
            self.show_status(f"Fehler: Keine Verbrauchsdauer für '{product_name}' gefunden.")

        conn.close()
        self.display_shopping_list()

    def show_status(self, message):
        self.status_label.config(text=message)
        self.master.after(3000, lambda: self.status_label.config(text=""))

    def get_purchase_date(self):
        purchase_date = simpledialog.askstring("Einkaufsdatum", "Bitte geben Sie das Einkaufsdatum ein (YYYY-MM-DD):")
        return purchase_date

    def check_and_update_item(self, product_name, typical_duration, purchase_date):
        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM shopping_list WHERE product_name = ?', (product_name,))
        existing_item = cursor.fetchone()

        if existing_item:
            cursor.execute('UPDATE shopping_list SET last_purchase_date = ? WHERE product_name = ?',
                           (purchase_date, product_name))
        else:
            cursor.execute(
                'INSERT INTO shopping_list (product_name, typical_duration, last_purchase_date) VALUES (?, ?, ?)',
                (product_name, typical_duration, purchase_date))

        conn.commit()
        conn.close()

    def export_shopping_list(self):
        purchase_date = self.get_purchase_date()
        if not purchase_date:
            self.show_status("Export abgebrochen.")
            return

        conn = sqlite3.connect('shopping_list.db')
        cursor = conn.cursor()

        cursor.execute('SELECT product_name, typical_duration FROM current_shopping_list')
        items = cursor.fetchall()

        for item in items:
            product_name, typical_duration = item
            self.check_and_update_item(product_name, typical_duration, purchase_date)

        cursor.execute('DELETE FROM current_shopping_list')

        conn.commit()
        conn.close()

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
                    file.write(f"{item[0]} (Verbrauchsdauer: {item[1]} Tage)\n")
            self.show_status(f"Einkaufsliste wurde exportiert und Artikel wurden aktualisiert.")