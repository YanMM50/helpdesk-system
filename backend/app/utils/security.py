"""
utils/security.py — Utilitários de segurança

Responsável por:
1. Hash e verificação de senhas (bcrypt)
2. Geração e validação de tokens JWT
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

settings = get_settings()

# CryptContext configura o algoritmo de hash de senhas
# bcrypt é o padrão da indústria: lento o suficiente para dificultar brute force
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(senha: str) -> str:
    """Transforma a senha em um hash seguro. Nunca armazenar senha pura."""
    return pwd_context.hash(senha)


def verify_password(senha_pura: str, senha_hash: str) -> bool:
    """Compara a senha digitada com o hash armazenado."""
    return pwd_context.verify(senha_pura, senha_hash)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Gera um token JWT com os dados do usuário.

    JWT (JSON Web Token) = token assinado digitalmente.
    Contém: payload (dados) + assinatura (prova de autenticidade).
    Quem tiver a SECRET_KEY pode verificar que o token é legítimo.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> Optional[dict]:
    """
    Decodifica e valida um token JWT.
    Retorna None se inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None
