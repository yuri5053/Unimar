from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.usuario import Usuario

class IUsuarioRepository(ABC):
    
    @abstractmethod
    def salvar(self, usuario: Usuario) -> str:
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def buscar_todos(self) -> List[Usuario]:
        pass
    
    @abstractmethod
    def atualizar(self, usuario: Usuario) -> None:
        pass
    
    @abstractmethod
    def deletar(self, id: str) -> None:
        pass