"""
routers/auth.py — Endpoints de autenticação (login/logout)
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import LoginRequest, Token, UserResponse
from app.utils.security import verify_password, create_access_token
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=Token, summary="Realizar login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica o usuário e retorna um token JWT.

    Fluxo:
    1. Busca usuário pelo email
    2. Verifica a senha com bcrypt
    3. Gera token JWT
    4. Registra o último login
    """
    # Busca por email (sempre ativo)
    user = db.query(User).filter(
        User.email == dados.email,
        User.ativo == True
    ).first()

    # Erro genérico — não revelar se o email existe ou não (segurança)
    if not user or not verify_password(dados.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos."
        )

    # Registra último login
    user.ultimo_login = datetime.utcnow()
    db.commit()

    # Gera token com o ID do usuário como "subject"
    token = create_access_token(data={"sub": str(user.id)})

    return Token(
        access_token=token,
        token_type="bearer",
        usuario=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse, summary="Dados do usuário logado")
def me(current_user: User = Depends(get_current_user)):
    """Retorna os dados do usuário autenticado via token."""
    return current_user
