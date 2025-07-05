# Presentation Layer - Controllers

from flask import Blueprint, request, jsonify
from src.application.use_cases import (
    CriarLivroUseCase, BuscarLivrosUseCase, CriarUsuarioUseCase,
    EmprestarLivroUseCase, DevolverLivroUseCase, ListarEmprestimosUseCase, DoarLivroUseCase, DoarHorasUseCase
)
from src.application.dtos import LivroDTO, UsuarioDTO, EmprestimoRequestDTO, DevolucaoRequestDTO, DoacaoDTO, HorasDTO
from src.infrastructure.repositories import (
    SQLAlchemyLivroRepository, SQLAlchemyUsuarioRepository, SQLAlchemyEmprestimoRepository, SQLAlchemyDoacaoRepository, SQLAlchemyHorasRepository
)

# Criar blueprint para a API da biblioteca
biblioteca_bp = Blueprint('biblioteca', __name__)

# Instanciar repositories (Dependency Injection)
livro_repository = SQLAlchemyLivroRepository()
usuario_repository = SQLAlchemyUsuarioRepository()
emprestimo_repository = SQLAlchemyEmprestimoRepository()
doacao_repository = SQLAlchemyDoacaoRepository()
horas_repository = SQLAlchemyHorasRepository()

@biblioteca_bp.route('/livros', methods=['POST'])
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

@biblioteca_bp.route('/livros', methods=['GET'])
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

@biblioteca_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    """
    Endpoint para criar um novo usuário
    """
    try:
        data = request.get_json()
        
        # Validar dados de entrada
        if not data or not all(k in data for k in ('nome', 'email')):
            return jsonify({'erro': 'Dados obrigatórios: nome, email'}), 400
        
        # Criar DTO
        usuario_dto = UsuarioDTO(
            nome=data['nome'],
            email=data['email']
        )
        
        # Executar use case
        use_case = CriarUsuarioUseCase(usuario_repository)
        usuario_id = use_case.executar(usuario_dto)
        
        return jsonify({
            'mensagem': 'Usuário criado com sucesso',
            'id': usuario_id
        }), 201
        
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@biblioteca_bp.route('/emprestimos', methods=['POST'])
def emprestar_livro():
    """
    Endpoint para emprestar um livro
    """
    try:
        data = request.get_json()
        
        # Validar dados de entrada
        if not data or not all(k in data for k in ('livro_id', 'usuario_id')):
            return jsonify({'erro': 'Dados obrigatórios: livro_id, usuario_id'}), 400
        
        # Executar use case
        use_case = EmprestarLivroUseCase(livro_repository, usuario_repository, emprestimo_repository)
        emprestimo_id = use_case.executar(data['livro_id'], data['usuario_id'])
        
        return jsonify({
            'mensagem': 'Livro emprestado com sucesso',
            'emprestimo_id': emprestimo_id
        }), 201
        
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@biblioteca_bp.route('/emprestimos/<emprestimo_id>/devolver', methods=['PUT'])
def devolver_livro(emprestimo_id):
    """
    Endpoint para devolver um livro
    """
    try:
        # Executar use case
        use_case = DevolverLivroUseCase(livro_repository, emprestimo_repository)
        multa = use_case.executar(emprestimo_id)
        
        return jsonify({
            'mensagem': 'Livro devolvido com sucesso',
            'multa': multa
        }), 200
        
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@biblioteca_bp.route('/emprestimos', methods=['GET'])
def listar_emprestimos():
    """
    Endpoint para listar empréstimos
    """
    try:
        usuario_id = request.args.get('usuario_id')
        apenas_ativos = request.args.get('ativos', 'false').lower() == 'true'
        
        # Executar use case
        use_case = ListarEmprestimosUseCase(emprestimo_repository)
        emprestimos = use_case.executar(usuario_id, apenas_ativos)
        
        # Converter DTOs para dicionários
        emprestimos_dict = []
        for emprestimo in emprestimos:
            emprestimos_dict.append({
                'id': emprestimo.id,
                'livro_id': emprestimo.livro_id,
                'usuario_id': emprestimo.usuario_id,
                'data_emprestimo': emprestimo.data_emprestimo,
                'data_devolucao_prevista': emprestimo.data_devolucao_prevista,
                'data_devolucao_real': emprestimo.data_devolucao_real,
                'multa': emprestimo.multa,
                'esta_em_atraso': emprestimo.esta_em_atraso,
                'dias_atraso': emprestimo.dias_atraso
            })
        
        return jsonify({
            'emprestimos': emprestimos_dict,
            'total': len(emprestimos_dict)
        }), 200
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@biblioteca_bp.route('/doacoes', methods=['POST'])
def listar_doacoes():
    """
    Endpoint para doar um livro
    """
    try:
        data = request.get_json()
        
        # Validar dados de entrada
        if not data or not all(k in data for k in ('livro_id', 'usuario_id', 'data_doacao')):
            return jsonify({'erro': 'Dados obrigatórios: livro_id, usuario_id, data_doacao'}), 400
        
        # Criar DTO
        doacao_dto = DoacaoDTO(
            livro_id=data['livro_id'],
            usuario_id=data['usuario_id'],
            data_doacao=data['data_doacao']
        )
        
        # Executar use case
        use_case = DoarLivroUseCase(doacao_repository)
        doacao_id = use_case.executar(doacao_dto)
        
        return jsonify({
            'mensagem': 'Livro doado com sucesso',
            'doacao_id': doacao_id
        }), 201
        
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@biblioteca_bp.route('/doacaoes/horas', methods=['POST'])
def doar_horas():
    """
    Endpoint para doar horas
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('usuario_id', 'horas')):
            return jsonify({'erro': 'Dados obrigatórios: usuario_id, horas'}), 400
        # Criar DTO
        horas_dto = HorasDTO(
            usuario_id=data['usuario_id'],
            horas=data['horas']
        )
        # Executar use case
        use_case = DoarHorasUseCase(usuario_repository, horas_repository)
        creditos = use_case.executar(horas_dto)
        return jsonify({
            'mensagem': 'Horas doadas com sucesso',
            'creditos': creditos
        }), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500   

@biblioteca_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check
    """
    return jsonify({
        'status': 'OK',
        'mensagem': 'API da Biblioteca funcionando corretamente'
    }), 200

