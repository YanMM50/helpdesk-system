"""
schemas/user.py — Formatos de entrada e saída para usuários
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import NivelSuporte


class UserCreate(BaseModel):
    """Dados necessários para criar um usuário (recebidos via POST)."""
    nome: str
    email: EmailStr
    senha: str
    nivel_suporte: NivelSuporte = NivelSuporte.N1
    cargo: Optional[str] = None
    company_id: Optional[int] = None

    @field_validator("senha")
    @classmethod
    def senha_minimo(cls, v):
        if len(v) < 6:
            raise ValueError("A senha deve ter no mínimo 6 caracteres.")
        return v


class UserUpdate(BaseModel):
    """Dados para atualizar um usuário (campos opcionais)."""
    nome: Optional[str] = None
    cargo: Optional[str] = None
    nivel_suporte: Optional[NivelSuporte] = None
    company_id: Optional[int] = None
    ativo: Optional[bool] = None


class UserResponse(BaseModel):
    """Dados retornados pela API (nunca incluir senha_hash!)."""
    id: int
    nome: str
    email: str
    nivel_suporte: NivelSuporte
    cargo: Optional[str]
    company_id: Optional[int]
    ativo: bool
    criado_em: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Resposta do endpoint de login."""
    access_token: str
    token_type: str = "bearer"
    usuario: UserResponse


class LoginRequest(BaseModel):
    """Dados de login recebidos do frontend."""
    email: EmailStr
    senha: str
