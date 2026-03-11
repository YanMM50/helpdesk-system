"""
routers/users.py — CRUD de usuários
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.security import hash_password
from app.services.auth_service import get_current_user, require_admin

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.post("/", response_model=UserResponse, status_code=201, summary="Criar usuário")
def create_user(
    dados: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)  # Só admin pode criar usuários
):
    # Verifica se o email já existe
    if db.query(User).filter(User.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    user = User(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_password(dados.senha),
        nivel_suporte=dados.nivel_suporte,
        cargo=dados.cargo,
        company_id=dados.company_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=List[UserResponse], summary="Listar usuários")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(User).filter(User.ativo == True).all()


@router.get("/{user_id}", response_model=UserResponse, summary="Buscar usuário por ID")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user


@router.put("/{user_id}", response_model=UserResponse, summary="Atualizar usuário")
def update_user(
    user_id: int,
    dados: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Só admin pode editar outros usuários
    if current_user.id != user_id and current_user.nivel_suporte.value != "ADMIN":
        raise HTTPException(status_code=403, detail="Sem permissão.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(user, campo, valor)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204, summary="Desativar usuário")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    user.ativo = False  # Soft delete — nunca apaga do banco
    db.commit()
