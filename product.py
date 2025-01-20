from abstract_product import AbstractProduct

class Product(AbstractProduct):
    def __init__(self, name, typical_duration, price):
        self._name = name
        self._typical_duration = typical_duration
        self._price = price

    def get_details(self):
        return f"{self._name} (Verbrauchsdauer: {self._typical_duration} Tage, Preis: {self._price:.2f} €)"

    @property
    def name(self):
        return self._name

    @property
    def typical_duration(self):
        return self._typical_duration

    @property
    def price(self):
        return self._price
