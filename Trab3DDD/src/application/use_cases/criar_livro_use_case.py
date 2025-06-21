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