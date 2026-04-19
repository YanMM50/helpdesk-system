"""
schemas/ticket.py — Formatos de entrada e saída para chamados
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.ticket import PrioridadeChamado, StatusChamado, TipoAcao
from app.models.user import NivelSuporte
from app.schemas.user import UserResponse


class TicketCreate(BaseModel):
    titulo: str
    descricao: str
    prioridade: PrioridadeChamado = PrioridadeChamado.MEDIA
    company_id: Optional[int] = None
    equipamento_id: Optional[int] = None
    tecnico_id: Optional[int] = None


class TicketUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    prioridade: Optional[PrioridadeChamado] = None
    tecnico_id: Optional[int] = None
    equipamento_id: Optional[int] = None


class TicketStatusUpdate(BaseModel):
    """Atualiza só o status e/ou nível do chamado."""
    status: Optional[StatusChamado] = None
    nivel_atual: Optional[NivelSuporte] = None
    comentario: Optional[str] = None


class HistoryResponse(BaseModel):
    id: int
    tipo_acao: TipoAcao
    comentario: Optional[str]
    nivel_anterior: Optional[NivelSuporte]
    nivel_novo: Optional[NivelSuporte]
    status_anterior: Optional[StatusChamado]
    status_novo: Optional[StatusChamado]
    criado_em: datetime
    usuario: Optional[UserResponse]

    model_config = {"from_attributes": True}


class AttachmentResponse(BaseModel):
    id: int
    nome_original: str
    nome_arquivo: Optional[str]
    tipo_mime: Optional[str]
    tamanho_bytes: Optional[int]
    caminho: Optional[str]
    criado_em: datetime

    model_config = {"from_attributes": True}


class TicketResponse(BaseModel):
    id: int
    protocolo: Optional[str]
    titulo: str
    descricao: str
    prioridade: PrioridadeChamado
    status: StatusChamado
    nivel_atual: NivelSuporte
    solicitante_id: int
    tecnico_id: Optional[int]
    company_id: Optional[int]
    equipamento_id: Optional[int]
    avaliacao: Optional[int] = None
    data_abertura: datetime
    data_fechamento: Optional[datetime]
    prazo_sla: Optional[datetime]
    criado_em: datetime
    atualizado_em: datetime
    solicitante: Optional[UserResponse] = None
    tecnico: Optional[UserResponse] = None
    company_nome: Optional[str] = None
    equipamento_nome: Optional[str] = None

    model_config = {"from_attributes": True}


class TicketDetailResponse(TicketResponse):
    """Versão completa com histórico e anexos."""
    historico: List[HistoryResponse] = []
    attachments: List[AttachmentResponse] = []


class ComentarioCreate(BaseModel):
    comentario: str


class EncaminhamentoCreate(BaseModel):
    nivel_destino: NivelSuporte
    comentario: Optional[str] = None
