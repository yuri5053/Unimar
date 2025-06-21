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