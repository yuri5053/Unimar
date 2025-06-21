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