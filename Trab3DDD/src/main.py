from src.presentation.controllers.user_controller import router as user_router
from fastapi import FastAPI
from flask import Flask, jsonify
from flask_cors import CORS
from src.infrastructure.database.config import init_database
from src.presentation.controllers.livro_controller import livro_bp

app = FastAPI()

app.include_router(user_router)

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
