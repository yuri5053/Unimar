from fastapi import APIRouter, HTTPException
from dataclasses import asdict
from src.infrastructure.repositories.user_repository import UserRepository
from src.application.use_case.create_user_use_case import CreateUserUseCase
from src.application.use_case.list_users_use_case import ListUsersUseCase
from src.application.use_case.update_user_use_case import UpdateUserUseCase
from src.presentation.schemas.user_schema import UserCreateSchema, UserUpdateSchema

router = APIRouter()
user_repository = UserRepository()
create_user_use_case = CreateUserUseCase(user_repository)
list_users_use_case = ListUsersUseCase(user_repository)
update_user_use_case = UpdateUserUseCase(user_repository)

@router.post("/usuarios")
def criar_usuario(user: UserCreateSchema):
    try:
        novo_usuario = create_user_use_case.execute(user.dict())
        return asdict(novo_usuario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/usuarios")
def listar_usuarios():
    usuarios = list_users_use_case.execute()
    return [asdict(u) for u in usuarios]

@router.put("/usuarios/{user_id}")
def atualizar_usuario(user_id: str, user: UserUpdateSchema):
    try:
        usuario_atualizado = update_user_use_case.execute(user_id, user.dict(exclude_unset=True))
        return asdict(usuario_atualizado)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))