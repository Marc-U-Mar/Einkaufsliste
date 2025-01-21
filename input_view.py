import tkinter as tk
from tkinter import ttk

class InputView:
    def __init__(self, master):
        self.product_name = ttk.Entry(master)
        self.product_name.grid(row=0, column=1, padx=5, pady=5)

        self.typical_duration = ttk.Entry(master)
        self.typical_duration.grid(row=1, column=1, padx=5, pady=5)

        self.price = ttk.Entry(master)
        self.price.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(master, text="Produktname:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(master, text="Verbrauchsdauer (Tage):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(master, text="Preis:").grid(row=2, column=0, sticky="w", padx=5, pady=5)

    def get_input_values(self):
        return (
            self.product_name.get(),
            self.typical_duration.get(),
            self.price.get()
        )

    def clear_inputs(self):
        self.product_name.delete(0, tk.END)
        self.typical_duration.delete(0, tk.END)
        self.price.delete(0, tk.END)
