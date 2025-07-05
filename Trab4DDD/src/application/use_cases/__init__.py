# Application Layer - Use Cases

from typing import List, Optional
from src.domain.entities import Livro, Usuario, Emprestimo, Doacao, Horas
from src.domain.repositories import LivroRepository, UsuarioRepository, EmprestimoRepository, DoacaoRepository, HorasRepository
from src.domain.value_objects.isbn import ISBN
from src.domain.value_objects.email import Email
from src.application.dtos import LivroDTO, UsuarioDTO, EmprestimoDTO, DoacaoDTO, HorasDTO

class CriarLivroUseCase:
    """
    Use Case: Criar Livro
    Aplicando Clean Architecture: Use Case na camada de aplicação
    Aplicando SOLID: Single Responsibility Principle
    """
    
    def __init__(self, livro_repository: LivroRepository):
        self._livro_repository = livro_repository
    
    def executar(self, dto: LivroDTO) -> str:
        """
        Executa a criação de um novo livro
        """
        # Verificar se já existe livro com mesmo ISBN
        livro_existente = self._livro_repository.buscar_por_isbn(dto.isbn)
        if livro_existente:
            raise ValueError(f"Já existe um livro com ISBN {dto.isbn}")
        
        # Criar entidade Livro
        isbn = ISBN(dto.isbn)
        livro = Livro(
            id="",  # Será gerado automaticamente
            titulo=dto.titulo,
            autor=dto.autor,
            isbn=isbn
        )
        
        # Salvar no repositório
        self._livro_repository.salvar(livro)
        
        return livro.id

class BuscarLivrosUseCase:
    """
    Use Case: Buscar Livros
    """
    
    def __init__(self, livro_repository: LivroRepository):
        self._livro_repository = livro_repository
    
    def executar(self, apenas_disponiveis: bool = False) -> List[LivroDTO]:
        """
        Busca livros, opcionalmente apenas os disponíveis
        """
        if apenas_disponiveis:
            livros = self._livro_repository.buscar_disponiveis()
        else:
            livros = self._livro_repository.buscar_todos()
        
        return [self._livro_para_dto(livro) for livro in livros]
    
    def _livro_para_dto(self, livro: Livro) -> LivroDTO:
        return LivroDTO(
            id=livro.id,
            titulo=livro.titulo,
            autor=livro.autor,
            isbn=str(livro.isbn),
            disponivel=livro.disponivel
        )

class CriarUsuarioUseCase:
    """
    Use Case: Criar Usuario
    """
    
    def __init__(self, usuario_repository: UsuarioRepository):
        self._usuario_repository = usuario_repository
    
    def executar(self, dto: UsuarioDTO) -> str:
        """
        Executa a criação de um novo usuário
        """
        # Verificar se já existe usuário com mesmo email
        usuario_existente = self._usuario_repository.buscar_por_email(dto.email)
        if usuario_existente:
            raise ValueError(f"Já existe um usuário com email {dto.email}")
        
        # Criar entidade Usuario
        email = Email(dto.email)
        usuario = Usuario(
            id="",  # Será gerado automaticamente
            nome=dto.nome,
            email=email
        )
        
        # Salvar no repositório
        self._usuario_repository.salvar(usuario)
        
        return usuario.id

class EmprestarLivroUseCase:
    """
    Use Case: Emprestar Livro
    Aplicando DDD: Orquestra operações entre agregados
    """
    
    def __init__(
        self, 
        livro_repository: LivroRepository,
        usuario_repository: UsuarioRepository,
        emprestimo_repository: EmprestimoRepository
    ):
        self._livro_repository = livro_repository
        self._usuario_repository = usuario_repository
        self._emprestimo_repository = emprestimo_repository
    
    def executar(self, livro_id: str, usuario_id: str) -> str:
        """
        Executa o empréstimo de um livro
        """
        # Buscar livro
        livro = self._livro_repository.buscar_por_id(livro_id)
        if not livro:
            raise ValueError(f"Livro não encontrado: {livro_id}")
        
        # Buscar usuário
        usuario = self._usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError(f"Usuário não encontrado: {usuario_id}")
        
        # Verificar se usuário está ativo
        if not usuario.ativo:
            raise ValueError("Usuário não está ativo")
        
        # Emprestar livro (regra de domínio)
        livro.emprestar()
        
        # Criar empréstimo
        emprestimo = Emprestimo(
            id="",  # Será gerado automaticamente
            livro_id=livro_id,
            usuario_id=usuario_id,
            data_emprestimo=None,  # Será definida automaticamente
            data_devolucao_prevista=None  # Será calculada automaticamente
        )
        
        # Salvar alterações
        self._livro_repository.salvar(livro)
        self._emprestimo_repository.salvar(emprestimo)
        
        return emprestimo.id

class DevolverLivroUseCase:
    """
    Use Case: Devolver Livro
    Aplicando DDD: Orquestra devolução gerando multa para o usuário
    """
    
    def __init__(
        self,
        livro_repository: LivroRepository,
        emprestimo_repository: EmprestimoRepository,
        usuario_repository: UsuarioRepository
    ):
        self._livro_repository = livro_repository
        self._emprestimo_repository = emprestimo_repository
        self._usuario_repository = usuario_repository
    
    def executar(self, emprestimo_id: str) -> float:
        """
        Executa a devolução de um livro
        Retorna o valor da multa, se houver
        """
        # Buscar empréstimo
        emprestimo = self._emprestimo_repository.buscar_por_id(emprestimo_id)
        if not emprestimo:
            raise ValueError(f"Empréstimo não encontrado: {emprestimo_id}")
        
        # Buscar livro
        livro = self._livro_repository.buscar_por_id(emprestimo.livro_id)
        if not livro:
            raise ValueError(f"Livro não encontrado: {emprestimo.livro_id}")
        # Buscar Usuário
        usuario = self._usuario_repository.buscar_por_id(emprestimo.usuario_id)
        if not usuario:
            raise ValueError(f"Usuário não encontrado: {emprestimo.usuario_id}")
        
        # Devolver livro (regras de domínio)
        emprestimo.devolver()
        livro.devolver()
        
        # Salvar alterações
        self._emprestimo_repository.salvar(emprestimo)
        self._livro_repository.salvar(livro)

        if usuario.creditos < emprestimo.multa:
            return emprestimo.multa
        else:
            usuario.creditos -= emprestimo.multa
            self._usuario_repository.salvar(usuario)
            return usuario.creditos

class ListarEmprestimosUseCase:
    """
    Use Case: Listar Empréstimos
    """
    
    def __init__(self, emprestimo_repository: EmprestimoRepository):
        self._emprestimo_repository = emprestimo_repository
    
    def executar(self, usuario_id: Optional[str] = None, apenas_ativos: bool = False) -> List[EmprestimoDTO]:
        """
        Lista empréstimos, opcionalmente filtrados por usuário ou apenas ativos
        """
        if usuario_id:
            emprestimos = self._emprestimo_repository.buscar_por_usuario(usuario_id)
        elif apenas_ativos:
            emprestimos = self._emprestimo_repository.buscar_ativos()
        else:
            emprestimos = self._emprestimo_repository.buscar_todos()
        
        return [self._emprestimo_para_dto(emprestimo) for emprestimo in emprestimos]
    
    def _emprestimo_para_dto(self, emprestimo: Emprestimo) -> EmprestimoDTO:
        return EmprestimoDTO(
            id=emprestimo.id,
            livro_id=emprestimo.livro_id,
            usuario_id=emprestimo.usuario_id,
            data_emprestimo=emprestimo.data_emprestimo.isoformat(),
            data_devolucao_prevista=emprestimo.data_devolucao_prevista.isoformat(),
            data_devolucao_real=emprestimo.data_devolucao_real.isoformat() if emprestimo.data_devolucao_real else None,
            multa=emprestimo.multa,
            esta_em_atraso=emprestimo.esta_em_atraso,
            dias_atraso=emprestimo.dias_atraso
        )

class DoarLivroUseCase:
    """
    Use Case: Doar Livro
    Aplicar DDD: Orquestra doação, gerando créditos para o usuário'
    """

    def __init__(
        self,
        livro_repository: LivroRepository,
        usuario_repository: UsuarioRepository,
        doacao_repository: DoacaoRepository
    ):
        self._livro_repository = livro_repository
        self._usuario_repository = usuario_repository
        self._doacao_repository = doacao_repository
    
    def executar(self, dto: DoacaoDTO) -> float:
        """
        Executa a doação de um livro
        """
        # Buscar livro
        livro = self._livro_repository.buscar_por_id(dto.livro_id)
        if not livro:
            raise ValueError(f"Livro não encontrado: {dto.livro_id}")
        
        # Buscar usuário
        usuario = self._usuario_repository.buscar_por_id(dto.usuario_id)
        if not usuario:
            raise ValueError(f"Usuário não encontrado: {dto.usuario_id}")
        
        # Criar doação
        doacao = Doacao(
            id="",  # Será gerado automaticamente
            livro_id=dto.livro_id,
            usuario_id=dto.usuario_id,
            data_doacao=None,  # Será definida automaticamente
            creditos=dto.creditos
        )
        
        # Salvar no repositório
        self._doacao_repository.salvar(doacao)

        # Atualizar créditos do usuário
        usuario.creditos += doacao.creditos
        self._usuario_repository.salvar(usuario)
        
        return usuario.creditos
    
class DoarHorasUseCase:
    """
    Use Case: Doar Horas
    Aplicar DDD: Orquestra doação de horas, gerando créditos para o usuário'
    """

    def __init__(
        self,
        horas_repository: HorasRepository,
        usuario_repository: UsuarioRepository
    ):
        self._horas_repository = horas_repository
        self._usuario_repository = usuario_repository
    
    def executar(self, dto: HorasDTO) -> float:
        """
        Executa a doação de horas
        """
        # Buscar usuário
        usuario = self._usuario_repository.buscar_por_id(dto.usuario_id)
        if not usuario:
            raise ValueError(f"Usuário não encontrado: {dto.usuario_id}")
        
        # Criar doação de horas
        horas = Horas(
            id="",  # Será gerado automaticamente
            usuario_id=dto.usuario_id,
            horas=dto.horas
        )
        
        # Salvar no repositório
        self._horas_repository.salvar(horas)

        # Atualizar créditos do usuário
        usuario.creditos += horas.creditos 
        self._usuario_repository.salvar(usuario)
        
        return usuario.creditos