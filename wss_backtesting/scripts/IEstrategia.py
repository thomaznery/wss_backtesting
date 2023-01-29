from abc import ABC, abstractmethod
from contabil.tradebook import TradeBook

class IEstrategia(ABC):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()        
  
    @abstractmethod
    def execute(self, *kwargs):        
        raise NotImplementedError
    