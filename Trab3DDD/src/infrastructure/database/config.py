from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Instância global do SQLAlchemy
db = SQLAlchemy()


def init_database(app: Flask) -> None:
    """
    Inicializa configuração do banco de dados
    """
    # Configuração do banco SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(basedir, '..', '..', 'database', 'app.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Criar tabelas
    with app.app_context():
        db.create_all()