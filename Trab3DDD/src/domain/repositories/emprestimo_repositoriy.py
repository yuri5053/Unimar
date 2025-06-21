from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.emprestimo import Emprestimo

class IEmprestimoRepository(ABC):
    
    @abstractmethod
    def salvar(self, emprestimo: Emprestimo) -> str:
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Emprestimo]:
        pass
    
    @abstractmethod
    def buscar_por_usuario(self, usuario_id: str) -> List[Emprestimo]:
        pass
    
    @abstractmethod
    def buscar_ativos(self) -> List[Emprestimo]:
        pass
    
    @abstractmethod
    def buscar_todos(self) -> List[Emprestimo]:
        pass
    
    @abstractmethod
    def atualizar(self, emprestimo: Emprestimo) -> None:
        pass