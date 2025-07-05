import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.presentation.controllers import biblioteca_bp
from src.infrastructure.database.models import LivroModel, UsuarioModel, EmprestimoModel

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS para permitir requisições de qualquer origem
CORS(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(biblioteca_bp, url_prefix='/api/biblioteca')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Criar tabelas
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/api/docs')
def api_docs():
    """
    Documentação básica da API
    """
    docs = {
        "titulo": "API da Biblioteca - Demonstração DDD",
        "versao": "1.0.0",
        "descricao": "API RESTful para gestão de biblioteca aplicando Clean Architecture, SOLID, Design Patterns e DDD",
        "endpoints": {
            "livros": {
                "POST /api/biblioteca/livros": "Criar novo livro",
                "GET /api/biblioteca/livros": "Listar livros (query param: ?disponiveis=true)",
            },
            "usuarios": {
                "POST /api/biblioteca/usuarios": "Criar novo usuário",
            },
            "emprestimos": {
                "POST /api/biblioteca/emprestimos": "Emprestar livro",
                "PUT /api/biblioteca/emprestimos/{id}/devolver": "Devolver livro",
                "GET /api/biblioteca/emprestimos": "Listar empréstimos (query params: ?usuario_id=X&ativos=true)",
            },
            "utilitarios": {
                "GET /api/biblioteca/health": "Health check da API",
                "GET /api/docs": "Esta documentação"
            }
        },
        "exemplos": {
            "criar_livro": {
                "url": "POST /api/biblioteca/livros",
                "body": {
                    "titulo": "Clean Architecture",
                    "autor": "Robert C. Martin",
                    "isbn": "978-0134494166"
                }
            },
            "criar_usuario": {
                "url": "POST /api/biblioteca/usuarios", 
                "body": {
                    "nome": "João Silva",
                    "email": "joao@email.com"
                }
            },
            "emprestar_livro": {
                "url": "POST /api/biblioteca/emprestimos",
                "body": {
                    "livro_id": "uuid-do-livro",
                    "usuario_id": "uuid-do-usuario"
                }
            }
        },
        "conceitos_aplicados": [
            "Clean Architecture (4 camadas)",
            "Princípios SOLID",
            "Design Patterns (Repository, Strategy)",
            "Domain-Driven Design (Entities, Value Objects, Aggregates)",
            "Dependency Injection",
            "Separation of Concerns"
        ]
    }
    
    return jsonify(docs)

if __name__ == '__main__':
    print("🚀 Iniciando API da Biblioteca...")
    print("📚 Demonstração de Clean Architecture + SOLID + Design Patterns + DDD")
    print("🌐 Acesse http://localhost:5001/api/docs para ver a documentação")
    print("💡 Health check: http://localhost:5001/api/biblioteca/health")
    app.run(host='0.0.0.0', port=5001, debug=True)

