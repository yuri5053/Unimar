# Domain Layer - Entities

from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass
from src.domain.value_objects.isbn import ISBN
from src.domain.value_objects.email import Email


@dataclass
class Livro:
    """
    Entity: Livro
    Representa um livro no domínio da biblioteca.
    Aplicando DDD: Entity com identidade única e comportamentos de domínio.
    """
    id: str
    titulo: str
    autor: str
    isbn: ISBN
    disponivel: bool = True
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
    
    def emprestar(self) -> None:
        """
        Regra de negócio: Um livro só pode ser emprestado se estiver disponível
        """
        if not self.disponivel:
            raise ValueError("Livro não está disponível para empréstimo")
        self.disponivel = False
    
    def devolver(self) -> None:
        """
        Regra de negócio: Devolver um livro o torna disponível novamente
        """
        self.disponivel = True
    
    def __eq__(self, other):
        if not isinstance(other, Livro):
            return False
        return self.id == other.id

@dataclass
class Usuario:
    """
    Entity: Usuario
    Representa um usuário da biblioteca.
    """
    id: str
    nome: str
    email: Email
    creditos: float = 0.0
    ativo: bool = True
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
    
    def desativar(self) -> None:
        """
        Regra de negócio: Desativar usuário
        """
        self.ativo = False
    
    def ativar(self) -> None:
        """
        Regra de negócio: Ativar usuário
        """
        self.ativo = True
    
    def __eq__(self, other):
        if not isinstance(other, Usuario):
            return False
        return self.id == other.id

@dataclass
class Emprestimo:
    """
    Entity: Emprestimo
    Representa um empréstimo de livro.
    Aggregate Root que controla a consistência do empréstimo.
    """
    id: str
    livro_id: str
    usuario_id: str
    data_emprestimo: datetime
    data_devolucao_prevista: datetime
    data_devolucao_real: Optional[datetime] = None
    multa: float = 0.0
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        if not self.data_emprestimo:
            self.data_emprestimo = datetime.now()
        if not self.data_devolucao_prevista:
            self.data_devolucao_prevista = self.data_emprestimo + timedelta(days=14)
    
    def devolver(self) -> None:
        """
        Regra de negócio: Processar devolução e calcular multa se necessário
        """
        if self.data_devolucao_real:
            raise ValueError("Livro já foi devolvido")
        
        self.data_devolucao_real = datetime.now()
        
        # Calcular multa por atraso (R$ 1,00 por dia)
        if self.data_devolucao_real > self.data_devolucao_prevista:
            dias_atraso = (self.data_devolucao_real - self.data_devolucao_prevista).days
            self.multa = dias_atraso * 1.0
    
    @property
    def esta_em_atraso(self) -> bool:
        """
        Verifica se o empréstimo está em atraso
        """
        if self.data_devolucao_real:
            return False
        return datetime.now() > self.data_devolucao_prevista
    
    @property
    def dias_atraso(self) -> int:
        """
        Calcula quantos dias de atraso
        """
        if not self.esta_em_atraso:
            return 0
        return (datetime.now() - self.data_devolucao_prevista).days
    
    def __eq__(self, other):
        if not isinstance(other, Emprestimo):
            return False
        return self.id == other.id

@dataclass
class Doacao:
    """
    Entity: Doacao
    Representa uma doação de livro.
    """
    id: str
    livro_id: str
    usuario_id: str
    data_doacao: datetime
    creditos: float = 0.0

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        if not self.data_doacao:
            self.data_doacao = datetime.now()
    

    def processar_creditos(self) -> None:
        self.creditos += 20.0  # Exemplo: cada doação gera 20 créditos para o usuário

@dataclass
class Horas:
    """
    Entity: Doacao
    Representa uma doação de livro.
    """
    id: str
    usuario_id: str
    horas: int
    data: datetime
    tipo: str
    creditos: float = 0.0

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        if not self.data:
            self.data = datetime.now()
    
    def gerar_creditos(self) -> None:
        """
        Regra de negócio: Gerar créditos com base nas horas registradas
        """
        if self.tipo == 'organização':
            self.creditos += (self.horas * 5.0)  # Exemplo: cada hora gera 5 créditos para o usuário
        elif self.tipo == 'palestra':
            self.creditos += (self.horas * 10.0) # Exemplo: cada hora de palestra gera 10 créditos para o usuário
        else:
            self.creditos += (self.horas * 2.0)  # Exemplo: cada hora de outra atividade gera 2 créditos para o usuário
