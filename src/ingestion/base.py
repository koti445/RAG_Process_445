from abc import ABC, abstractmethod

from src.domain.models import LoadedDocument

class BaseLoader(ABC):
    
    @abstractmethod
    def load(self, source: str, **kwargs) -> list[LoadedDocument]:
        raise NotImplementedError
        
    def supports(self, source_type: str) -> bool:
        return False
        
        