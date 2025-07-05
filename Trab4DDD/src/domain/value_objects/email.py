# Domain Layer - Value Objects

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Value Object: Email
    Representa um endereço de email válido.
    Aplicando DDD: Value Object imutável com validação.
    """
    valor: str
    
    def __post_init__(self):
        if not self._is_valid_email(self.valor):
            raise ValueError(f"Email inválido: {self.valor}")
    
    def _is_valid_email(self, email: str) -> bool:
        """
        Valida formato de email usando regex
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def __str__(self):
        return self.valor
    
    @property
    def dominio(self) -> str:
        """
        Retorna o domínio do email
        """
        return self.valor.split('@')[1]
    
    @property
    def usuario(self) -> str:
        """
        Retorna a parte do usuário do email
        """
        return self.valor.split('@')[0]

