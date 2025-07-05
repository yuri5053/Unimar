# Domain Layer - Value Objects

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ISBN:
    """
    Value Object: ISBN
    Representa um ISBN válido.
    Aplicando DDD: Value Object imutável com validação de domínio.
    """
    valor: str
    
    def __post_init__(self):
        if not self._is_valid_isbn(self.valor):
            raise ValueError(f"ISBN inválido: {self.valor}")
    
    def _is_valid_isbn(self, isbn: str) -> bool:
        """
        Valida formato ISBN-10 ou ISBN-13
        """
        # Remove hífens e espaços
        isbn_clean = re.sub(r'[-\s]', '', isbn)
        
        # Verifica se é ISBN-10 ou ISBN-13
        if len(isbn_clean) == 10:
            return self._validate_isbn10(isbn_clean)
        elif len(isbn_clean) == 13:
            return self._validate_isbn13(isbn_clean)
        
        return False
    
    def _validate_isbn10(self, isbn: str) -> bool:
        """Valida ISBN-10"""
        if not re.match(r'^\d{9}[\dX]$', isbn):
            return False
        
        total = 0
        for i, char in enumerate(isbn[:-1]):
            total += int(char) * (10 - i)
        
        check_digit = isbn[-1]
        if check_digit == 'X':
            total += 10
        else:
            total += int(check_digit)
        
        return total % 11 == 0
    
    def _validate_isbn13(self, isbn: str) -> bool:
        """Valida ISBN-13"""
        if not re.match(r'^\d{13}$', isbn):
            return False
        
        total = 0
        for i, char in enumerate(isbn[:-1]):
            multiplier = 1 if i % 2 == 0 else 3
            total += int(char) * multiplier
        
        check_digit = (10 - (total % 10)) % 10
        return check_digit == int(isbn[-1])
    
    def __str__(self):
        return self.valor

