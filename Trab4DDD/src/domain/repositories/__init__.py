# Domain Layer - Repository Interfaces

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Livro, Usuario, Emprestimo, Doacao, Horas


class LivroRepository(ABC):
    """
    Repository Interface para Livro
    Aplicando DDD: Repository Pattern - Interface no domínio, implementação na infraestrutura
    Aplicando SOLID: Dependency Inversion Principle
    """
    
    @abstractmethod
    def salvar(self, livro: Livro) -> None:
        """Salva um livro"""
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Livro]:
        """Busca livro por ID"""
        pass
    
    @abstractmethod
    def buscar_por_isbn(self, isbn: str) -> Optional[Livro]:
        """Busca livro por ISBN"""
        pass
    
    @abstractmethod
    def buscar_todos(self) -> List[Livro]:
        """Busca todos os livros"""
        pass
    
    @abstractmethod
    def buscar_disponiveis(self) -> List[Livro]:
        """Busca livros disponíveis"""
        pass
    
    @abstractmethod
    def deletar(self, id: str) -> None:
        """Deleta um livro"""
        pass

class UsuarioRepository(ABC):
    """
    Repository Interface para Usuario
    """
    
    @abstractmethod
    def salvar(self, usuario: Usuario) -> None:
        """Salva um usuário"""
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """Busca usuário por ID"""
        pass
    
    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca usuário por email"""
        pass
    
    @abstractmethod
    def buscar_todos(self) -> List[Usuario]:
        """Busca todos os usuários"""
        pass
    
    @abstractmethod
    def deletar(self, id: str) -> None:
        """Deleta um usuário"""
        pass

class EmprestimoRepository(ABC):
    """
    Repository Interface para Emprestimo
    """
    
    @abstractmethod
    def salvar(self, emprestimo: Emprestimo) -> None:
        """Salva um empréstimo"""
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Emprestimo]:
        """Busca empréstimo por ID"""
        pass
    
    @abstractmethod
    def buscar_por_usuario(self, usuario_id: str) -> List[Emprestimo]:
        """Busca empréstimos de um usuário"""
        pass
    
    @abstractmethod
    def buscar_por_livro(self, livro_id: str) -> List[Emprestimo]:
        """Busca empréstimos de um livro"""
        pass
    
    @abstractmethod
    def buscar_ativos(self) -> List[Emprestimo]:
        """Busca empréstimos ativos (não devolvidos)"""
        pass
    
    @abstractmethod
    def buscar_em_atraso(self) -> List[Emprestimo]:
        """Busca empréstimos em atraso"""
        pass
    
    @abstractmethod
    def deletar(self, id: str) -> None:
        """Deleta um empréstimo"""
        pass

class DoacaoRepository(ABC):
    """
    Repository Interface para Doação
    """
    @abstractmethod
    def salvar(self, doacao: Doacao) -> None:
        """Salva uma doação"""
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: str) -> Doacao:
        """Busca doação por ID"""
        pass
    
    @abstractmethod
    def buscar_por_livro(self, livro_id: str) -> Doacao:
        """Busca doações de um livro"""
        pass
    @abstractmethod
    def buscar_por_usuario(self, usuario_id: str) -> List[Doacao]:
        """Busca doações de um usuário"""
        pass
    
    @abstractmethod
    def buscar_todos(self) -> List[Doacao]:
        """Busca todas as doações"""
        pass
    
    @abstractmethod
    def deletar(self, id: str) -> None:
        """Deleta uma doação"""
        pass

class HorasRepository(ABC):
    """
    Repository Interface para Horas
    """
    @abstractmethod
    def salvar(self, horas: Horas) -> None:
        """Salva uma hora"""
        pass
    @abstractmethod
    def buscar_por_id(self, id: str) -> Horas:
        """Busca horas por ID"""
        pass
    @abstractmethod
    def buscar_por_usuario(self, usuario_id: str) -> List[Horas]:
        """Busca horas de um usuário"""
        pass
    @abstractmethod
    def buscar_todas(self) -> List[Horas]:
        """Busca todas as horas"""
        pass
    @abstractmethod
    def deletar(self, id: str) -> None:
        """Deleta uma hora"""
        pass