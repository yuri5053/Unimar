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