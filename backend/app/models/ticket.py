"""
models/ticket.py — Modelos das tabelas: tickets, ticket_history, attachments
"""
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models.user import NivelSuporte


class PrioridadeChamado(str, enum.Enum):
    BAIXA   = "BAIXA"
    MEDIA   = "MEDIA"
    ALTA    = "ALTA"
    CRITICA = "CRITICA"


class StatusChamado(str, enum.Enum):
    ABERTO              = "ABERTO"
    EM_ANALISE          = "EM_ANALISE"
    EM_ATENDIMENTO      = "EM_ATENDIMENTO"
    AGUARDANDO_CLIENTE  = "AGUARDANDO_CLIENTE"
    RESOLVIDO           = "RESOLVIDO"
    FECHADO             = "FECHADO"


class TipoAcao(str, enum.Enum):
    ABERTURA        = "ABERTURA"
    COMENTARIO      = "COMENTARIO"
    MUDANCA_STATUS  = "MUDANCA_STATUS"
    ENCAMINHAMENTO  = "ENCAMINHAMENTO"
    RESOLUCAO       = "RESOLUCAO"
    FECHAMENTO      = "FECHAMENTO"
    EDICAO          = "EDICAO"


class Ticket(Base):
    __tablename__ = "tickets"

    id              = Column(Integer, primary_key=True, index=True)
    titulo          = Column(String(200), nullable=False)
    descricao       = Column(Text, nullable=False)
    prioridade      = Column(Enum(PrioridadeChamado), nullable=False, default=PrioridadeChamado.MEDIA)
    status          = Column(Enum(StatusChamado), nullable=False, default=StatusChamado.ABERTO)
    nivel_atual     = Column(Enum(NivelSuporte), nullable=False, default=NivelSuporte.N1)
    protocolo       = Column(String(20), unique=True)

    solicitante_id  = Column(Integer, ForeignKey("users.id"), nullable=False)
    tecnico_id      = Column(Integer, ForeignKey("users.id"), nullable=True)
    company_id      = Column(Integer, ForeignKey("companies.id"), nullable=True)
    equipamento_id  = Column(Integer, ForeignKey("equipments.id"), nullable=True)

    avaliacao       = Column(Integer, nullable=True)  # 1-5 estrelas (CSAT)

    data_abertura   = Column(DateTime(timezone=True), server_default=func.now())
    data_fechamento = Column(DateTime(timezone=True), nullable=True)
    prazo_sla       = Column(DateTime(timezone=True), nullable=True)
    criado_em       = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em   = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    solicitante = relationship("User", foreign_keys=[solicitante_id], back_populates="tickets_abertos")
    tecnico     = relationship("User", foreign_keys=[tecnico_id], back_populates="tickets_atribuidos")
    company     = relationship("Company", back_populates="tickets")
    equipamento = relationship("Equipment", back_populates="tickets")
    historico   = relationship("TicketHistory", back_populates="ticket", cascade="all, delete-orphan", order_by="TicketHistory.criado_em")
    attachments = relationship("Attachment", back_populates="ticket", cascade="all, delete-orphan")


class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id              = Column(Integer, primary_key=True, index=True)
    ticket_id       = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    usuario_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    tipo_acao       = Column(Enum(TipoAcao), nullable=False)
    comentario      = Column(Text)
    nivel_anterior  = Column(Enum(NivelSuporte), nullable=True)
    nivel_novo      = Column(Enum(NivelSuporte), nullable=True)
    status_anterior = Column(Enum(StatusChamado), nullable=True)
    status_novo     = Column(Enum(StatusChamado), nullable=True)
    criado_em       = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    ticket  = relationship("Ticket", back_populates="historico")
    usuario = relationship("User", back_populates="historico")


class Attachment(Base):
    __tablename__ = "attachments"

    id             = Column(Integer, primary_key=True, index=True)
    ticket_id      = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    usuario_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    nome_original  = Column(String(255), nullable=False)
    nome_arquivo   = Column(String(255), nullable=False)
    tipo_mime      = Column(String(100))
    tamanho_bytes  = Column(BigInteger)
    caminho        = Column(String(500), nullable=False)
    criado_em      = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    ticket  = relationship("Ticket", back_populates="attachments")
    usuario = relationship("User", back_populates="attachments")
