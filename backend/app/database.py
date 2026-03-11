"""
database.py — Conexão com o banco de dados via SQLAlchemy

SQLAlchemy é um ORM (Object Relational Mapper):
- Permite trabalhar com o banco usando classes Python
- Não precisamos escrever SQL manualmente para operações simples
- Protege contra SQL Injection automaticamente
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

settings = get_settings()

# Engine = a "conexão" com o banco de dados
# pool_pre_ping=True testa a conexão antes de usar (evita erros de timeout)
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,          # conexões simultâneas no pool
    max_overflow=20,       # conexões extras permitidas
    echo=settings.debug,   # se True, mostra SQL no terminal (útil para debug)
)

# SessionLocal é a "fábrica" de sessões de banco
# Cada requisição HTTP deve ter sua própria sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base é a classe pai de todos os nossos modelos (tabelas)
Base = declarative_base()


def get_db():
    """
    Dependency Injection do FastAPI.
    Garante que a sessão é aberta e fechada corretamente em cada requisição.
    O 'yield' transforma a função em um gerador — FastAPI cuida do resto.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
