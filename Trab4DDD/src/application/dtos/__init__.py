"""
DTOs (Data Transfer Objects) - Camada de Aplicação
Versão Completa com todos os DTOs necessários para os controllers
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class LivroDTO:
    """DTO para transferência de dados de Livro"""
    # Campos obrigatórios primeiro
    titulo: str
    autor: str
    isbn: str
    
    # Campos opcionais depois
    id: Optional[str] = None
    disponivel: bool = True
    editora: Optional[str] = None
    ano_publicacao: Optional[int] = None
    numero_paginas: Optional[int] = None
    categoria: Optional[str] = None

@dataclass
class UsuarioDTO:
    """DTO para transferência de dados de Usuario"""
    # Campos obrigatórios primeiro
    nome: str
    email: str
    
    # Campos opcionais depois
    id: Optional[str] = None
    ativo: bool = True
    emprestimos_ativos: int = 0
    multas_pendentes: float = 0.0
    data_cadastro: Optional[datetime] = None

@dataclass
class EmprestimoDTO:
    """DTO para transferência de dados de Emprestimo"""
    # Campos obrigatórios primeiro
    livro_id: str
    usuario_id: str
    
    # Campos opcionais depois
    id: Optional[str] = None
    data_emprestimo: Optional[datetime] = None
    data_devolucao_prevista: Optional[datetime] = None
    data_devolucao_real: Optional[datetime] = None
    multa: float = 0.0
    devolvido: bool = False

@dataclass
class DoacaoDTO:
    """DTO para transferência de dados de Doacao"""
    # Campos obrigatórios primeiro
    livro_id: str
    doador_nome: str
    doador_email: str
    
    # Campos opcionais depois
    id: Optional[str] = None
    data_doacao: Optional[datetime] = None
    observacoes: Optional[str] = None

# DTOs para requests da API (ESTES ESTAVAM FALTANDO!)
@dataclass
class EmprestimoRequestDTO:
    """DTO para request de empréstimo"""
    livro_id: str
    usuario_id: str

@dataclass
class DevolucaoRequestDTO:
    """DTO para request de devolução"""
    emprestimo_id: str
    data_devolucao: Optional[datetime] = None
    observacoes: Optional[str] = None

@dataclass
class CriarLivroRequest:
    """Request para criar livro"""
    titulo: str
    autor: str
    isbn: str
    editora: Optional[str] = None
    ano_publicacao: Optional[int] = None
    numero_paginas: Optional[int] = None
    categoria: Optional[str] = None

@dataclass
class CriarUsuarioRequest:
    """Request para criar usuário"""
    nome: str
    email: str

@dataclass
class CriarEmprestimoRequest:
    """Request para criar empréstimo"""
    livro_id: str
    usuario_id: str

@dataclass
class ApiResponse:
    """Response padrão da API"""
    # Campos obrigatórios primeiro
    success: bool
    message: str
    
    # Campos opcionais depois
    data: Optional[dict] = None
    errors: Optional[List[str]] = None

@dataclass
class PaginationDTO:
    """DTO para paginação"""
    # Campos obrigatórios primeiro
    page: int
    per_page: int
    total: int
    
    # Campos opcionais depois
    has_next: bool = False
    has_prev: bool = False
    next_page: Optional[int] = None
    prev_page: Optional[int] = None

# Funções auxiliares para conversão
def livro_to_dto(livro) -> LivroDTO:
    """Converte Entity Livro para DTO"""
    return LivroDTO(
        titulo=livro.titulo,
        autor=livro.autor,
        isbn=str(livro.isbn),
        id=livro.id,
        disponivel=livro.disponivel,
        editora=getattr(livro, 'editora', None),
        ano_publicacao=getattr(livro, 'ano_publicacao', None),
        numero_paginas=getattr(livro, 'numero_paginas', None),
        categoria=getattr(livro, 'categoria', None)
    )

def usuario_to_dto(usuario) -> UsuarioDTO:
    """Converte Entity Usuario para DTO"""
    return UsuarioDTO(
        nome=usuario.nome,
        email=str(usuario.email),
        id=usuario.id,
        ativo=usuario.ativo,
        emprestimos_ativos=usuario.emprestimos_ativos,
        multas_pendentes=usuario.multas_pendentes,
        data_cadastro=getattr(usuario, 'data_cadastro', None)
    )

def emprestimo_to_dto(emprestimo) -> EmprestimoDTO:
    """Converte Entity Emprestimo para DTO"""
    return EmprestimoDTO(
        livro_id=emprestimo.livro_id,
        usuario_id=emprestimo.usuario_id,
        id=emprestimo.id,
        data_emprestimo=emprestimo.data_emprestimo,
        data_devolucao_prevista=emprestimo.data_devolucao_prevista,
        data_devolucao_real=emprestimo.data_devolucao_real,
        multa=emprestimo.multa,
        devolvido=emprestimo.devolvido
    )

@dataclass
class HorasDTO:
    """DTO para transferência de dados de Horas"""
    # Campos obrigatórios primeiro
    usuario_id: str
    horas: float
    
    # Campos opcionais depois
    id: Optional[str] = None
    data: Optional[datetime] = None
    creditos: Optional[float] = None
