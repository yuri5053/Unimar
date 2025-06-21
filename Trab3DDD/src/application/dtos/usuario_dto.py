from dataclasses import dataclass
from typing import Optional

@dataclass
class UsuarioDTO:
    """
    DTO para transferência de dados de Usuario
    """
    id: Optional[str] = None
    nome: str = ""
    email: str = ""
    ativo: bool = True