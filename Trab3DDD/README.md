# 🚀 UNIMAR AULAS DE DDD: Criando API com Clean Architecture + SOLID + DDD Professor Victor Icoma

## Tutorial Completo - Do Zero à Produção

Este guia ensina como criar uma API REST aplicando Clean Architecture, princípios SOLID, Design Patterns e Domain-Driven Design (DDD) do zero.

---

## 📋 Pré-requisitos

- Python 3.11+ instalado
- Conhecimento básico de Python e Flask
- Editor de código (VS Code, PyCharm, etc.)
- Terminal/Command Prompt

---

## 🏗️ ETAPA 1: Configuração Inicial do Projeto

### 1.1 Criar Diretório e Ambiente Virtual

```bash
# Criar diretório do projeto
mkdir biblioteca-api
cd biblioteca-api

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Verificar ativação (deve mostrar (venv) no prompt)
which python  # Linux/macOS
where python   # Windows
```

### 1.2 Instalar Dependências Básicas

```bash
# Instalar Flask e dependências
pip install flask flask-cors flask-sqlalchemy

# Criar arquivo de dependências
pip freeze > requirements.txt
```

### 1.3 Criar Estrutura de Diretórios

```bash
# Criar estrutura Clean Architecture
mkdir -p src/{domain/{entities,value_objects,repositories,services},application/{use_cases,dtos},infrastructure/{database,repositories},presentation/controllers}

# Criar arquivos __init__.py
touch src/__init__.py
touch src/domain/__init__.py
touch src/domain/entities/__init__.py
touch src/domain/value_objects/__init__.py
touch src/domain/repositories/__init__.py
touch src/domain/services/__init__.py
touch src/application/__init__.py
touch src/application/use_cases/__init__.py
touch src/application/dtos/__init__.py
touch src/infrastructure/__init__.py
touch src/infrastructure/database/__init__.py
touch src/infrastructure/repositories/__init__.py
touch src/presentation/__init__.py
touch src/presentation/controllers/__init__.py

# Criar diretório para banco de dados
mkdir -p src/database
```

---

## 🎯 ETAPA 2: Implementar Camada de Domínio (DDD)

### 2.1 Criar Value Objects

**Arquivo: `src/domain/value_objects/isbn.py`**
```python
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ISBN:
    """
    Value Object para ISBN
    Aplicando DDD: Objeto de valor imutável com validação
    """
    value: str
    
    def __post_init__(self):
        if not self._is_valid_isbn(self.value):
            raise ValueError(f"ISBN inválido: {self.value}")
    
    def _is_valid_isbn(self, isbn: str) -> bool:
        """Valida formato ISBN-10 ou ISBN-13"""
        # Remove hífens e espaços
        clean_isbn = re.sub(r'[-\s]', '', isbn)
        
        # Verifica ISBN-10 ou ISBN-13
        if len(clean_isbn) == 10:
            return self._validate_isbn10(clean_isbn)
        elif len(clean_isbn) == 13:
            return self._validate_isbn13(clean_isbn)
        return False
    
    def _validate_isbn10(self, isbn: str) -> bool:
        """Valida ISBN-10"""
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
        """Valida ISBN-13"""
        if not isbn.isdigit():
            return False
        
        total = sum(int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(isbn[:-1]))
        check_digit = (10 - (total % 10)) % 10
        
        return check_digit == int(isbn[-1])
    
    def __str__(self) -> str:
        return self.value
```

**Arquivo: `src/domain/value_objects/email.py`**
```python
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    """
    Value Object para Email
    Aplicando DDD: Objeto de valor imutável com validação
    """
    value: str
    
    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValueError(f"Email inválido: {self.value}")
    
    def _is_valid_email(self, email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def __str__(self) -> str:
        return self.value
```

### 2.2 Criar Entities

**Arquivo: `src/domain/entities/livro.py`**
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid
from ..value_objects.isbn import ISBN

@dataclass
class Livro:
    """
    Entity Livro
    Aplicando DDD: Entidade com identidade e comportamentos de domínio
    """
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
        """
        Comportamento de domínio: emprestar livro
        Aplicando DDD: Lógica de negócio na entidade
        """
        if not self.disponivel:
            raise ValueError("Livro não está disponível para empréstimo")
        self.disponivel = False
    
    def devolver(self) -> None:
        """
        Comportamento de domínio: devolver livro
        """
        if self.disponivel:
            raise ValueError("Livro já está disponível")
        self.disponivel = True
    
    def __eq__(self, other) -> bool:
        """Igualdade baseada na identidade (ID)"""
        if not isinstance(other, Livro):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
```

**Arquivo: `src/domain/entities/usuario.py`**
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid
from ..value_objects.email import Email

@dataclass
class Usuario:
    """
    Entity Usuario
    Aplicando DDD: Entidade com identidade e comportamentos
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nome: str = ""
    email: Email = None
    ativo: bool = True
    data_criacao: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.nome:
            raise ValueError("Nome é obrigatório")
        if not self.email:
            raise ValueError("Email é obrigatório")
    
    def desativar(self) -> None:
        """
        Comportamento de domínio: desativar usuário
        """
        if not self.ativo:
            raise ValueError("Usuário já está inativo")
        self.ativo = False
    
    def ativar(self) -> None:
        """
        Comportamento de domínio: ativar usuário
        """
        if self.ativo:
            raise ValueError("Usuário já está ativo")
        self.ativo = True
    
    def pode_emprestar(self) -> bool:
        """
        Regra de negócio: usuário pode emprestar livros
        """
        return self.ativo
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Usuario):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
```

**Arquivo: `src/domain/entities/emprestimo.py`**
```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import uuid

@dataclass
class Emprestimo:
    """
    Entity Emprestimo (Aggregate Root)
    Aplicando DDD: Agregado que mantém consistência
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    livro_id: str = ""
    usuario_id: str = ""
    data_emprestimo: datetime = field(default_factory=datetime.utcnow)
    data_devolucao_prevista: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=14))
    data_devolucao_real: Optional[datetime] = None
    multa: float = 0.0
    
    def __post_init__(self):
        if not self.livro_id:
            raise ValueError("ID do livro é obrigatório")
        if not self.usuario_id:
            raise ValueError("ID do usuário é obrigatório")
    
    def devolver(self) -> float:
        """
        Comportamento de domínio: devolver livro e calcular multa
        Aplicando DDD: Lógica de negócio complexa no agregado
        """
        if self.data_devolucao_real:
            raise ValueError("Livro já foi devolvido")
        
        self.data_devolucao_real = datetime.utcnow()
        self.multa = self._calcular_multa()
        return self.multa
    
    def _calcular_multa(self) -> float:
        """
        Regra de negócio: calcular multa por atraso
        R$ 1,00 por dia de atraso
        """
        if not self.data_devolucao_real:
            return 0.0
        
        if self.data_devolucao_real <= self.data_devolucao_prevista:
            return 0.0
        
        dias_atraso = (self.data_devolucao_real - self.data_devolucao_prevista).days
        return dias_atraso * 1.0  # R$ 1,00 por dia
    
    @property
    def esta_em_atraso(self) -> bool:
        """
        Propriedade calculada: verifica se está em atraso
        """
        if self.data_devolucao_real:
            return False  # Já foi devolvido
        return datetime.utcnow() > self.data_devolucao_prevista
    
    @property
    def dias_atraso(self) -> int:
        """
        Propriedade calculada: dias de atraso
        """
        if not self.esta_em_atraso:
            return 0
        return (datetime.utcnow() - self.data_devolucao_prevista).days
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Emprestimo):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
```

### 2.3 Atualizar __init__.py do Domain

**Arquivo: `src/domain/entities/__init__.py`**
```python
# Domain Layer - Entities

from .livro import Livro
from .usuario import Usuario
from .emprestimo import Emprestimo

__all__ = ['Livro', 'Usuario', 'Emprestimo']
```

**Arquivo: `src/domain/value_objects/__init__.py`**
```python
# Domain Layer - Value Objects

from .isbn import ISBN
from .email import Email

__all__ = ['ISBN', 'Email']
```

---

## 🔧 ETAPA 3: Implementar Repository Interfaces (SOLID - D)

### 3.1 Criar Interfaces dos Repositories

**Arquivo: `src/domain/repositories/livro_repository.py`**
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.livro import Livro

class ILivroRepository(ABC):
    """
    Interface do Repository de Livro
    Aplicando SOLID: Dependency Inversion Principle
    Aplicando DDD: Repository pattern
    """
    
    @abstractmethod
    def salvar(self, livro: Livro) -> str:
        """Salva um livro e retorna o ID"""
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Livro]:
        """Busca livro por ID"""
        pass
    
    @abstractmethod
    def buscar_todos(self) -> List[Livro]:
        """Busca todos os livros"""
        pass
    
    @abstractmethod
    def buscar_disponiveis(self) -> List[Livro]:
        """Busca apenas livros disponíveis"""
        pass
    
    @abstractmethod
    def atualizar(self, livro: Livro) -> None:
        """Atualiza um livro"""
        pass
    
    @abstractmethod
    def deletar(self, id: str) -> None:
        """Deleta um livro"""
        pass
```

**Arquivo: `src/domain/repositories/usuario_repository.py`**
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.usuario import Usuario

class IUsuarioRepository(ABC):
    """
    Interface do Repository de Usuario
    Aplicando SOLID: Dependency Inversion Principle
    """
    
    @abstractmethod
    def salvar(self, usuario: Usuario) -> str:
        """Salva um usuário e retorna o ID"""
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
    def atualizar(self, usuario: Usuario) -> None:
        """Atualiza um usuário"""
        pass
    
    @abstractmethod
    def deletar(self, id: str) -> None:
        """Deleta um usuário"""
        pass
```

**Arquivo: `src/domain/repositories/emprestimo_repository.py`**
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.emprestimo import Emprestimo

class IEmprestimoRepository(ABC):
    """
    Interface do Repository de Emprestimo
    """
    
    @abstractmethod
    def salvar(self, emprestimo: Emprestimo) -> str:
        """Salva um empréstimo e retorna o ID"""
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
    def buscar_ativos(self) -> List[Emprestimo]:
        """Busca empréstimos ativos (não devolvidos)"""
        pass
    
    @abstractmethod
    def buscar_todos(self) -> List[Emprestimo]:
        """Busca todos os empréstimos"""
        pass
    
    @abstractmethod
    def atualizar(self, emprestimo: Emprestimo) -> None:
        """Atualiza um empréstimo"""
        pass
```

### 3.2 Atualizar __init__.py dos Repositories

**Arquivo: `src/domain/repositories/__init__.py`**
```python
# Domain Layer - Repository Interfaces

from .livro_repository import ILivroRepository
from .usuario_repository import IUsuarioRepository
from .emprestimo_repository import IEmprestimoRepository

__all__ = ['ILivroRepository', 'IUsuarioRepository', 'IEmprestimoRepository']
```

---

## 📦 ETAPA 4: Implementar Camada de Aplicação

### 4.1 Criar DTOs

**Arquivo: `src/application/dtos/livro_dto.py`**
```python
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
```

**Arquivo: `src/application/dtos/usuario_dto.py`**
```python
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
```

**Arquivo: `src/application/dtos/emprestimo_dto.py`**
```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EmprestimoDTO:
    """
    DTO para transferência de dados de Emprestimo
    """
    id: Optional[str] = None
    livro_id: str = ""
    usuario_id: str = ""
    data_emprestimo: Optional[datetime] = None
    data_devolucao_prevista: Optional[datetime] = None
    data_devolucao_real: Optional[datetime] = None
    multa: float = 0.0
    esta_em_atraso: bool = False
    dias_atraso: int = 0
```

### 4.2 Criar Use Cases

**Arquivo: `src/application/use_cases/criar_livro_use_case.py`**
```python
from ..dtos.livro_dto import LivroDTO
from ...domain.entities.livro import Livro
from ...domain.value_objects.isbn import ISBN
from ...domain.repositories.livro_repository import ILivroRepository

class CriarLivroUseCase:
    """
    Use Case para criar livro
    Aplicando Clean Architecture: Lógica de aplicação isolada
    Aplicando SOLID: Single Responsibility Principle
    """
    
    def __init__(self, livro_repository: ILivroRepository):
        self._livro_repository = livro_repository
    
    def executar(self, livro_dto: LivroDTO) -> str:
        """
        Executa o caso de uso de criar livro
        """
        # Validar dados
        if not livro_dto.titulo:
            raise ValueError("Título é obrigatório")
        if not livro_dto.autor:
            raise ValueError("Autor é obrigatório")
        if not livro_dto.isbn:
            raise ValueError("ISBN é obrigatório")
        
        # Criar Value Object
        isbn = ISBN(livro_dto.isbn)
        
        # Criar Entity
        livro = Livro(
            titulo=livro_dto.titulo,
            autor=livro_dto.autor,
            isbn=isbn
        )
        
        # Salvar via Repository
        return self._livro_repository.salvar(livro)
```

**Arquivo: `src/application/use_cases/buscar_livros_use_case.py`**
```python
from typing import List
from ..dtos.livro_dto import LivroDTO
from ...domain.repositories.livro_repository import ILivroRepository

class BuscarLivrosUseCase:
    """
    Use Case para buscar livros
    """
    
    def __init__(self, livro_repository: ILivroRepository):
        self._livro_repository = livro_repository
    
    def executar(self, apenas_disponiveis: bool = False) -> List[LivroDTO]:
        """
        Executa busca de livros
        """
        if apenas_disponiveis:
            livros = self._livro_repository.buscar_disponiveis()
        else:
            livros = self._livro_repository.buscar_todos()
        
        # Converter Entities para DTOs
        return [
            LivroDTO(
                id=livro.id,
                titulo=livro.titulo,
                autor=livro.autor,
                isbn=str(livro.isbn),
                disponivel=livro.disponivel
            )
            for livro in livros
        ]
```

**Arquivo: `src/application/use_cases/emprestar_livro_use_case.py`**
```python
from ...domain.entities.emprestimo import Emprestimo
from ...domain.repositories.livro_repository import ILivroRepository
from ...domain.repositories.usuario_repository import IUsuarioRepository
from ...domain.repositories.emprestimo_repository import IEmprestimoRepository

class EmprestarLivroUseCase:
    """
    Use Case para emprestar livro
    Aplicando DDD: Orquestração de múltiplos agregados
    """
    
    def __init__(
        self,
        livro_repository: ILivroRepository,
        usuario_repository: IUsuarioRepository,
        emprestimo_repository: IEmprestimoRepository
    ):
        self._livro_repository = livro_repository
        self._usuario_repository = usuario_repository
        self._emprestimo_repository = emprestimo_repository
    
    def executar(self, livro_id: str, usuario_id: str) -> str:
        """
        Executa empréstimo de livro
        """
        # Buscar livro
        livro = self._livro_repository.buscar_por_id(livro_id)
        if not livro:
            raise ValueError("Livro não encontrado")
        
        # Buscar usuário
        usuario = self._usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        
        # Validar regras de negócio
        if not usuario.pode_emprestar():
            raise ValueError("Usuário não pode emprestar livros")
        
        if not livro.disponivel:
            raise ValueError("Livro não está disponível")
        
        # Emprestar livro (comportamento de domínio)
        livro.emprestar()
        
        # Criar empréstimo
        emprestimo = Emprestimo(
            livro_id=livro_id,
            usuario_id=usuario_id
        )
        
        # Salvar mudanças
        self._livro_repository.atualizar(livro)
        emprestimo_id = self._emprestimo_repository.salvar(emprestimo)
        
        return emprestimo_id
```

### 4.3 Atualizar __init__.py da Application

**Arquivo: `src/application/dtos/__init__.py`**
```python
# Application Layer - DTOs

from .livro_dto import LivroDTO
from .usuario_dto import UsuarioDTO
from .emprestimo_dto import EmprestimoDTO

__all__ = ['LivroDTO', 'UsuarioDTO', 'EmprestimoDTO']
```

**Arquivo: `src/application/use_cases/__init__.py`**
```python
# Application Layer - Use Cases

from .criar_livro_use_case import CriarLivroUseCase
from .buscar_livros_use_case import BuscarLivrosUseCase
from .emprestar_livro_use_case import EmprestarLivroUseCase

__all__ = ['CriarLivroUseCase', 'BuscarLivrosUseCase', 'EmprestarLivroUseCase']
```

---

## 🏭 ETAPA 5: Implementar Camada de Infraestrutura

### 5.1 Configurar SQLAlchemy

**Arquivo: `src/infrastructure/database/config.py`**
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Instância global do SQLAlchemy
db = SQLAlchemy()

def init_database(app: Flask) -> None:
    """
    Inicializa configuração do banco de dados
    """
    # Configuração do banco SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(basedir, '..', '..', 'database', 'app.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar SQLAlchemy
    db.init_app(app)
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
```

### 5.2 Criar Models SQLAlchemy

**Arquivo: `src/infrastructure/database/models.py`**
```python
from datetime import datetime
from .config import db

class LivroModel(db.Model):
    """
    Model SQLAlchemy para Livro
    Aplicando Clean Architecture: Models na camada de infraestrutura
    """
    __tablename__ = 'livros'
    
    id = db.Column(db.String(36), primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(17), unique=True, nullable=False)
    disponivel = db.Column(db.Boolean, default=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Livro {self.titulo}>'

class UsuarioModel(db.Model):
    """
    Model SQLAlchemy para Usuario
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.String(36), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'

class EmprestimoModel(db.Model):
    """
    Model SQLAlchemy para Emprestimo
    """
    __tablename__ = 'emprestimos'
    
    id = db.Column(db.String(36), primary_key=True)
    livro_id = db.Column(db.String(36), db.ForeignKey('livros.id'), nullable=False)
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False)
    data_emprestimo = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_devolucao_prevista = db.Column(db.DateTime, nullable=False)
    data_devolucao_real = db.Column(db.DateTime, nullable=True)
    multa = db.Column(db.Float, default=0.0, nullable=False)
    
    # Relacionamentos
    livro = db.relationship('LivroModel', backref='emprestimos')
    usuario = db.relationship('UsuarioModel', backref='emprestimos')
    
    def __repr__(self):
        return f'<Emprestimo {self.id}>'
```

### 5.3 Implementar Repository Concreto

**Arquivo: `src/infrastructure/repositories/sqlalchemy_livro_repository.py`**
```python
from typing import List, Optional
from ...domain.entities.livro import Livro
from ...domain.value_objects.isbn import ISBN
from ...domain.repositories.livro_repository import ILivroRepository
from ..database.models import LivroModel
from ..database.config import db

class SQLAlchemyLivroRepository(ILivroRepository):
    """
    Implementação concreta do Repository de Livro usando SQLAlchemy
    Aplicando SOLID: Dependency Inversion Principle
    Aplicando Design Pattern: Repository Pattern
    """
    
    def salvar(self, livro: Livro) -> str:
        """Salva um livro no banco de dados"""
        model = LivroModel(
            id=livro.id,
            titulo=livro.titulo,
            autor=livro.autor,
            isbn=str(livro.isbn),
            disponivel=livro.disponivel,
            data_criacao=livro.data_criacao
        )
        
        db.session.add(model)
        db.session.commit()
        
        return model.id
    
    def buscar_por_id(self, id: str) -> Optional[Livro]:
        """Busca livro por ID"""
        model = LivroModel.query.get(id)
        if not model:
            return None
        
        return self._model_to_entity(model)
    
    def buscar_todos(self) -> List[Livro]:
        """Busca todos os livros"""
        models = LivroModel.query.all()
        return [self._model_to_entity(model) for model in models]
    
    def buscar_disponiveis(self) -> List[Livro]:
        """Busca apenas livros disponíveis"""
        models = LivroModel.query.filter_by(disponivel=True).all()
        return [self._model_to_entity(model) for model in models]
    
    def atualizar(self, livro: Livro) -> None:
        """Atualiza um livro"""
        model = LivroModel.query.get(livro.id)
        if not model:
            raise ValueError("Livro não encontrado")
        
        model.titulo = livro.titulo
        model.autor = livro.autor
        model.isbn = str(livro.isbn)
        model.disponivel = livro.disponivel
        
        db.session.commit()
    
    def deletar(self, id: str) -> None:
        """Deleta um livro"""
        model = LivroModel.query.get(id)
        if model:
            db.session.delete(model)
            db.session.commit()
    
    def _model_to_entity(self, model: LivroModel) -> Livro:
        """Converte Model para Entity"""
        return Livro(
            id=model.id,
            titulo=model.titulo,
            autor=model.autor,
            isbn=ISBN(model.isbn),
            disponivel=model.disponivel,
            data_criacao=model.data_criacao
        )
```

---

## 🌐 ETAPA 6: Implementar Camada de Apresentação

### 6.1 Criar Controllers

**Arquivo: `src/presentation/controllers/livro_controller.py`**
```python
from flask import Blueprint, request, jsonify
from ...application.use_cases.criar_livro_use_case import CriarLivroUseCase
from ...application.use_cases.buscar_livros_use_case import BuscarLivrosUseCase
from ...application.dtos.livro_dto import LivroDTO
from ...infrastructure.repositories.sqlalchemy_livro_repository import SQLAlchemyLivroRepository

# Criar blueprint
livro_bp = Blueprint('livros', __name__)

# Dependency Injection (simplificado)
livro_repository = SQLAlchemyLivroRepository()

@livro_bp.route('/livros', methods=['POST'])
def criar_livro():
    """
    Endpoint para criar um novo livro
    Aplicando Clean Architecture: Controller na camada de apresentação
    """
    try:
        data = request.get_json()
        
        # Validar dados de entrada
        if not data or not all(k in data for k in ('titulo', 'autor', 'isbn')):
            return jsonify({'erro': 'Dados obrigatórios: titulo, autor, isbn'}), 400
        
        # Criar DTO
        livro_dto = LivroDTO(
            titulo=data['titulo'],
            autor=data['autor'],
            isbn=data['isbn']
        )
        
        # Executar use case
        use_case = CriarLivroUseCase(livro_repository)
        livro_id = use_case.executar(livro_dto)
        
        return jsonify({
            'mensagem': 'Livro criado com sucesso',
            'id': livro_id
        }), 201
        
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@livro_bp.route('/livros', methods=['GET'])
def listar_livros():
    """
    Endpoint para listar livros
    """
    try:
        apenas_disponiveis = request.args.get('disponiveis', 'false').lower() == 'true'
        
        # Executar use case
        use_case = BuscarLivrosUseCase(livro_repository)
        livros = use_case.executar(apenas_disponiveis)
        
        # Converter DTOs para dicionários
        livros_dict = []
        for livro in livros:
            livros_dict.append({
                'id': livro.id,
                'titulo': livro.titulo,
                'autor': livro.autor,
                'isbn': livro.isbn,
                'disponivel': livro.disponivel
            })
        
        return jsonify({
            'livros': livros_dict,
            'total': len(livros_dict)
        }), 200
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500
```

### 6.2 Criar Aplicação Principal

**Arquivo: `src/main.py`**
```python
from flask import Flask, jsonify
from flask_cors import CORS
from infrastructure.database.config import init_database
from presentation.controllers.livro_controller import livro_bp

def create_app():
    """
    Factory function para criar aplicação Flask
    Aplicando Clean Architecture: Configuração na camada de apresentação
    """
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
    
    # Configurar CORS
    CORS(app)
    
    # Inicializar banco de dados
    init_database(app)
    
    # Registrar blueprints
    app.register_blueprint(livro_bp, url_prefix='/api')
    
    # Rota de documentação
    @app.route('/api/docs')
    def api_docs():
        """Documentação básica da API"""
        docs = {
            "titulo": "API da Biblioteca - Demonstração DDD",
            "versao": "1.0.0",
            "descricao": "API RESTful aplicando Clean Architecture, SOLID, Design Patterns e DDD",
            "endpoints": {
                "livros": {
                    "POST /api/livros": "Criar novo livro",
                    "GET /api/livros": "Listar livros",
                    "GET /api/livros?disponiveis=true": "Listar apenas livros disponíveis"
                }
            },
            "exemplo_criar_livro": {
                "url": "POST /api/livros",
                "body": {
                    "titulo": "Clean Architecture",
                    "autor": "Robert C. Martin",
                    "isbn": "978-0134494166"
                }
            }
        }
        return jsonify(docs)
    
    # Health check
    @app.route('/api/health')
    def health_check():
        """Health check da API"""
        return jsonify({
            'status': 'OK',
            'mensagem': 'API da Biblioteca funcionando corretamente'
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Iniciando API da Biblioteca...")
    print("📚 Demonstração de Clean Architecture + SOLID + Design Patterns + DDD")
    print("🌐 Acesse http://localhost:5001/api/docs para ver a documentação")
    print("💡 Health check: http://localhost:5001/api/health")
    app.run(host='0.0.0.0', port=5001, debug=True)
```

---

## 🧪 ETAPA 7: Criar Testes

### 7.1 Teste da Estrutura

**Arquivo: `test_structure.py`**
```python
# Teste simples da estrutura DDD

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from domain.entities.livro import Livro
    from domain.entities.usuario import Usuario
    from domain.value_objects.isbn import ISBN
    from domain.value_objects.email import Email
    print("✅ Importações do domínio funcionando")
    
    # Teste de criação de entidades
    isbn = ISBN("978-0134494166")
    livro = Livro(titulo="Clean Architecture", autor="Robert Martin", isbn=isbn)
    print(f"✅ Livro criado: {livro.titulo}")
    
    email = Email("teste@email.com")
    usuario = Usuario(nome="João Silva", email=email)
    print(f"✅ Usuário criado: {usuario.nome}")
    
    # Teste de comportamentos
    livro.emprestar()
    print(f"✅ Livro emprestado: disponível = {livro.disponivel}")
    
    livro.devolver()
    print(f"✅ Livro devolvido: disponível = {livro.disponivel}")
    
    print("🎉 Estrutura DDD funcionando corretamente!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
```

---

## 🚀 ETAPA 8: Executar e Testar

### 8.1 Executar a Aplicação

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows

# Testar estrutura
python test_structure.py

# Executar aplicação
python src/main.py
```

### 8.2 Testar API

```bash
# Health check
curl http://localhost:5001/api/health

# Documentação
curl http://localhost:5001/api/docs

# Criar livro
curl -X POST http://localhost:5001/api/livros \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Clean Architecture",
    "autor": "Robert C. Martin",
    "isbn": "978-0134494166"
  }'

# Listar livros
curl http://localhost:5001/api/livros
```

---

## 🎯 Conceitos Implementados

### ✅ Clean Architecture
- **4 camadas** bem definidas e isoladas
- **Dependency Rule** respeitada (dependências apontam para dentro)
- **Separation of Concerns** aplicada

### ✅ Princípios SOLID
- **S** - Single Responsibility: Cada classe tem uma responsabilidade
- **O** - Open/Closed: Extensível via interfaces
- **L** - Liskov Substitution: Implementações substituíveis
- **I** - Interface Segregation: Interfaces específicas
- **D** - Dependency Inversion: Dependências via abstrações

### ✅ Design Patterns
- **Repository Pattern**: Abstração da camada de dados
- **Strategy Pattern**: Diferentes implementações via interfaces
- **Dependency Injection**: Injeção de dependências

### ✅ Domain-Driven Design
- **Entities**: Livro, Usuario, Emprestimo com identidade
- **Value Objects**: ISBN, Email imutáveis com validação
- **Aggregates**: Emprestimo como aggregate root
- **Repositories**: Interfaces no domínio, implementação na infraestrutura
- **Use Cases**: Lógica de aplicação isolada

---

## 🔄 Próximos Passos

1. **Implementar mais Use Cases** (criar usuário, devolver livro)
2. **Adicionar mais Controllers** (usuário, empréstimo)
3. **Implementar testes unitários** com pytest
4. **Adicionar validação de entrada** com schemas
5. **Implementar autenticação** JWT
6. **Containerizar com Docker**
7. **Adicionar logging e monitoramento**

---

**Parabéns! 🎉 Você criou uma API completa aplicando os melhores padrões de arquitetura de software!**

