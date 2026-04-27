"""
services/auth_service.py — Lógica de autenticação e autorização

Dependency Injection no FastAPI:
- Funções marcadas com Depends() são executadas automaticamente
- O FastAPI injeta o resultado como parâmetro nas rotas
- Isso evita repetição de código de autenticação em cada rota
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, NivelSuporte
from app.utils.security import decode_token

# HTTPBearer extrai o token do header: Authorization: Bearer <token>
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Valida o token JWT e retorna o usuário autenticado.
    Usada como dependência em rotas protegidas:
        @router.get("/...", dependencies=[Depends(get_current_user)])
    """
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido.")

    user = db.query(User).filter(User.id == int(user_id), User.ativo == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado ou inativo.")

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Rejeita acesso se o usuário não for ADMIN."""
    if current_user.nivel_suporte != NivelSuporte.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores."
        )
    return current_user


def require_n2_or_above(current_user: User = Depends(get_current_user)) -> User:
    """Rejeita acesso se o usuário for N1."""
    niveis_permitidos = [NivelSuporte.N2, NivelSuporte.N3, NivelSuporte.ADMIN]
    if current_user.nivel_suporte not in niveis_permitidos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a técnicos N2, N3 ou administradores."
        )
    return current_user


def require_n3_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Permite acesso apenas a N3 e ADMIN."""
    niveis_permitidos = [NivelSuporte.N3, NivelSuporte.ADMIN]
    if current_user.nivel_suporte not in niveis_permitidos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a N3 e administradores."
        )
    return current_user
