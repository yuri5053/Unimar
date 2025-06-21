from src.domain.entities.usuario import Usuario
from src.domain.value_objects.email import Email
from dataclasses import asdict
from fastapi import APIRouter, HTTPException

router = APIRouter()

class UserRepository:
    def __init__(self):
        self.users = []

    def create(self, user_data):
        if "nome" not in user_data or not user_data["nome"]:
            raise ValueError("Nome é obrigatório")
        if "email" not in user_data or not user_data["email"]:
            raise ValueError("Email é obrigatório")
        usuario = Usuario(
            nome=user_data["nome"],
            email=Email(user_data["email"])
        )
        self.users.append(usuario)
        return usuario

    def list_all(self):
        return self.users

    def update(self, user_id, user_data):
        for usuario in self.users:
            if usuario.id == user_id:
                if "nome" in user_data and user_data["nome"]:
                    usuario.nome = user_data["nome"]
                if "email" in user_data and user_data["email"]:
                    usuario.email = Email(user_data["email"])
                return usuario
        raise ValueError("Usuário não encontrado")