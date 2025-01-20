class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product, last_purchase_date):
        self.products[product.name] = {
            "product": product,
            "last_purchase_date": last_purchase_date
        }

    def get_inventory(self):
        return self.products
