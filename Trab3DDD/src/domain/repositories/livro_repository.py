from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.livro import Livro

class ILivroRepository(ABC):
    
    @abstractmethod
    def salvar(self, livro: Livro) -> str:
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Livro]:
        pass
    
    @abstractmethod
    def buscar_todos(self) -> List[Livro]:
        pass
    
    @abstractmethod
    def buscar_disponiveis(self) -> List[Livro]:
        pass
    
    @abstractmethod
    def atualizar(self, livro: Livro) -> None:
        pass
    
    @abstractmethod
    def deletar(self, id: str) -> None:
        pass