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