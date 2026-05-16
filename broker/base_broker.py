from abc import ABC, abstractmethod

class BaseBroker(ABC):
    @abstractmethod
    def buy(self, ticker: str, quantity: int, price: float):
        pass

    @abstractmethod
    def sell(self, ticker: str, quantity: int, price: float):
        pass

    @abstractmethod
    def get_positions(self):
        pass
