"""
routers/auth.py — Endpoints de autenticação (login, cadastro, logout)
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, NivelSuporte, TipoUsuario
from app.schemas.user import LoginRequest, RegisterRequest, Token, UserResponse
from app.utils.security import verify_password, create_access_token, hash_password
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=Token, summary="Realizar login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == dados.email,
        User.ativo == True
    ).first()

    if not user or not verify_password(dados.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos."
        )

    user.ultimo_login = datetime.utcnow()
    db.commit()

    token = create_access_token(data={"sub": str(user.id)})

    return Token(
        access_token=token,
        token_type="bearer",
        usuario=UserResponse.model_validate(user)
    )


@router.post("/register", response_model=Token, status_code=201, summary="Cadastro de cliente")
def register(dados: RegisterRequest, db: Session = Depends(get_db)):
    """
    Cadastro público — qualquer pessoa pode se registrar como CLIENTE.
    Colaboradores (N1/N2/N3) são criados apenas pelo administrador.
    """
    if db.query(User).filter(User.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    user = User(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_password(dados.senha),
        nivel_suporte=NivelSuporte.N1,
        tipo_usuario=TipoUsuario.CLIENTE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})

    return Token(
        access_token=token,
        token_type="bearer",
        usuario=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse, summary="Dados do usuário logado")
def me(current_user: User = Depends(get_current_user)):
    return current_user
