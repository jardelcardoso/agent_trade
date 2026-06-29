from abc import ABC, abstractmethod

class BaseBroker(ABC):
    @abstractmethod
    def execute_order(self, symbol: str, action: str, quantity: float, price: float = None):
        pass
