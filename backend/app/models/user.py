"""
models/user.py — Modelo da tabela 'users'
"""
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class NivelSuporte(str, enum.Enum):
    N1    = "N1"
    N2    = "N2"
    N3    = "N3"
    ADMIN = "ADMIN"


class TipoUsuario(str, enum.Enum):
    CLIENTE     = "CLIENTE"
    COLABORADOR = "COLABORADOR"


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    nome          = Column(String(150), nullable=False)
    email         = Column(String(150), nullable=False, unique=True, index=True)
    senha_hash    = Column(String(255), nullable=False)
    nivel_suporte = Column(Enum(NivelSuporte), nullable=False, default=NivelSuporte.N1)
    tipo_usuario  = Column(Enum(TipoUsuario, create_type=False), nullable=False, default=TipoUsuario.COLABORADOR)
    cargo         = Column(String(100))
    company_id    = Column(Integer, ForeignKey("companies.id"), nullable=True)
    ativo         = Column(Boolean, default=True, nullable=False)
    ultimo_login  = Column(DateTime(timezone=True), nullable=True)
    criado_em     = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    company              = relationship("Company", back_populates="users")
    tickets_abertos      = relationship("Ticket", foreign_keys="Ticket.solicitante_id", back_populates="solicitante")
    tickets_atribuidos   = relationship("Ticket", foreign_keys="Ticket.tecnico_id", back_populates="tecnico")
    historico            = relationship("TicketHistory", back_populates="usuario")
    attachments          = relationship("Attachment", back_populates="usuario")
