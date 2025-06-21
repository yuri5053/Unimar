from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid
from ..value_objects.isbn import ISBN

@dataclass
class Livro:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    titulo: str = ""
    autor: str = ""
    isbn: ISBN = None
    disponivel: bool = True
    data_criacao: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.titulo:
            raise ValueError("Título é obrigatório")
        if not self.autor:
            raise ValueError("Autor é obrigatório")
        if not self.isbn:
            raise ValueError("ISBN é obrigatório")
    
    def emprestar(self) -> None:
        if not self.disponivel:
            raise ValueError("Livro não está disponível para empréstimo")
        self.disponivel = False
    
    def devolver(self) -> None:
        if self.disponivel:
            raise ValueError("Livro já está disponível")
        self.disponivel = True
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Livro):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)