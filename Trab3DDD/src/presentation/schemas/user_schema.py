from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreateSchema(BaseModel):
    nome: str
    email: EmailStr


class UserUpdateSchema(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
