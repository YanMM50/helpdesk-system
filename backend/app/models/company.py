"""
models/company.py — Modelo da tabela 'companies'

Cada classe aqui representa uma tabela no banco.
Cada atributo de classe representa uma coluna.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id            = Column(Integer, primary_key=True, index=True)
    nome          = Column(String(150), nullable=False)
    cnpj          = Column(String(18), unique=True)
    telefone      = Column(String(20))
    email         = Column(String(150))
    endereco      = Column(String(255))
    ativo         = Column(Boolean, default=True, nullable=False)
    criado_em     = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos (permite acessar users, equipments e tickets via Python)
    users      = relationship("User", back_populates="company")
    equipments = relationship("Equipment", back_populates="company")
    tickets    = relationship("Ticket", back_populates="company")
