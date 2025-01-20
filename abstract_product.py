from abc import ABC, abstractmethod

class AbstractProduct(ABC):
    @abstractmethod
    def get_details(self):
        pass
