from dataclasses import dataclass
from typing import Optional

@dataclass
class LivroDTO:
    """
    DTO para transferência de dados de Livro
    Aplicando Clean Architecture: Isolamento entre camadas
    """
    id: Optional[str] = None
    titulo: str = ""
    autor: str = ""
    isbn: str = ""
    disponivel: bool = True