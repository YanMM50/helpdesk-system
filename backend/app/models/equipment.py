"""
models/equipment.py — Modelo da tabela 'equipments'
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Equipment(Base):
    __tablename__ = "equipments"

    id            = Column(Integer, primary_key=True, index=True)
    nome          = Column(String(150), nullable=False)
    tipo          = Column(String(100))
    fabricante    = Column(String(100))
    modelo        = Column(String(100))
    numero_serie  = Column(String(100), unique=True)
    patrimonio    = Column(String(50))
    company_id    = Column(Integer, ForeignKey("companies.id"), nullable=True)
    responsavel_id= Column(Integer, ForeignKey("users.id"), nullable=True)
    ativo         = Column(Boolean, default=True, nullable=False)
    criado_em     = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    company    = relationship("Company", back_populates="equipments")
    responsavel= relationship("User", foreign_keys=[responsavel_id])
    tickets    = relationship("Ticket", back_populates="equipamento")
