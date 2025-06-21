import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ISBN:
    value: str
    
    def __post_init__(self):
        if not self._is_valid_isbn(self.value):
            raise ValueError(f"ISBN inválido: {self.value}")
    
    def _is_valid_isbn(self, isbn: str) -> bool:
        clean_isbn = re.sub(r'[-\s]', '', isbn)
        if len(clean_isbn) == 10:
            return self._validate_isbn10(clean_isbn)
        elif len(clean_isbn) == 13:
            return self._validate_isbn13(clean_isbn)
        return False
    
    def _validate_isbn10(self, isbn: str) -> bool:
        if not isbn[:-1].isdigit():
            return False
        
        total = sum(int(digit) * (10 - i) for i, digit in enumerate(isbn[:-1]))
        check_digit = isbn[-1]
        
        if check_digit.upper() == 'X':
            total += 10
        elif check_digit.isdigit():
            total += int(check_digit)
        else:
            return False
            
        return total % 11 == 0
    
    def _validate_isbn13(self, isbn: str) -> bool:
        if not isbn.isdigit():
            return False
        
        total = sum(int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(isbn[:-1]))
        check_digit = (10 - (total % 10)) % 10
        
        return check_digit == int(isbn[-1])
    
    def __str__(self) -> str:
        return self.value