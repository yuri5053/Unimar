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