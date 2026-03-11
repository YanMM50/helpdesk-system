"""
routers/tickets.py — Endpoints de chamados técnicos

Este é o roteador mais importante do sistema.
Contém toda a lógica de fluxo dos chamados.
"""
import os
import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.ticket import Ticket, TicketHistory, Attachment, StatusChamado, TipoAcao
from app.models.user import User, NivelSuporte
from app.schemas.ticket import (
    TicketCreate, TicketUpdate, TicketResponse, TicketDetailResponse,
    TicketStatusUpdate, ComentarioCreate, EncaminhamentoCreate
)
from app.services.auth_service import get_current_user
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/tickets", tags=["Chamados"])


def _registrar_historico(
    db: Session,
    ticket: Ticket,
    usuario: User,
    tipo_acao: TipoAcao,
    comentario: str = None,
    nivel_anterior: NivelSuporte = None,
    nivel_novo: NivelSuporte = None,
    status_anterior: StatusChamado = None,
    status_novo: StatusChamado = None,
):
    """
    Função auxiliar: registra uma entrada no histórico do chamado.
    Centralizar aqui evita repetição de código nos endpoints.
    """
    entry = TicketHistory(
        ticket_id=ticket.id,
        usuario_id=usuario.id,
        tipo_acao=tipo_acao,
        comentario=comentario,
        nivel_anterior=nivel_anterior,
        nivel_novo=nivel_novo,
        status_anterior=status_anterior,
        status_novo=status_novo,
    )
    db.add(entry)


# ============================================================
# CRIAR CHAMADO
# ============================================================

@router.post("/", response_model=TicketResponse, status_code=201, summary="Abrir chamado")
def create_ticket(
    dados: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Abre um novo chamado técnico.
    O protocolo é gerado automaticamente pelo trigger do banco.
    """
    ticket = Ticket(
        titulo=dados.titulo,
        descricao=dados.descricao,
        prioridade=dados.prioridade,
        status=StatusChamado.ABERTO,
        nivel_atual=NivelSuporte.N1,
        solicitante_id=current_user.id,
        tecnico_id=dados.tecnico_id,
        company_id=dados.company_id,
        equipamento_id=dados.equipamento_id,
    )
    db.add(ticket)
    db.flush()  # Gera o ID sem commitar, necessário para o trigger

    _registrar_historico(
        db=db, ticket=ticket, usuario=current_user,
        tipo_acao=TipoAcao.ABERTURA,
        comentario=f"Chamado aberto: {dados.descricao[:200]}"
    )

    db.commit()
    db.refresh(ticket)
    return ticket


# ============================================================
# LISTAR CHAMADOS
# ============================================================

@router.get("/", response_model=List[TicketResponse], summary="Listar chamados")
def list_tickets(
    status: Optional[StatusChamado] = Query(None),
    prioridade: Optional[str] = Query(None),
    nivel: Optional[NivelSuporte] = Query(None),
    tecnico_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista chamados com filtros opcionais.
    N1 vê apenas seus chamados ou os sem técnico.
    N2/N3/ADMIN veem todos.
    """
    query = db.query(Ticket)

    # Filtro por nível de acesso
    if current_user.nivel_suporte == NivelSuporte.N1:
        query = query.filter(
            (Ticket.tecnico_id == current_user.id) |
            (Ticket.solicitante_id == current_user.id)
        )

    if status:
        query = query.filter(Ticket.status == status)
    if prioridade:
        query = query.filter(Ticket.prioridade == prioridade)
    if nivel:
        query = query.filter(Ticket.nivel_atual == nivel)
    if tecnico_id:
        query = query.filter(Ticket.tecnico_id == tecnico_id)

    return query.order_by(Ticket.data_abertura.desc()).all()


# ============================================================
# BUSCAR CHAMADO INDIVIDUAL
# ============================================================

@router.get("/{ticket_id}", response_model=TicketDetailResponse, summary="Detalhes do chamado")
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    """Retorna chamado completo com histórico e anexos."""
    ticket = (
        db.query(Ticket)
        .options(
            joinedload(Ticket.historico).joinedload(TicketHistory.usuario),
            joinedload(Ticket.attachments)
        )
        .filter(Ticket.id == ticket_id)
        .first()
    )
    if not ticket:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")
    return ticket


# ============================================================
# EDITAR CHAMADO
# ============================================================

@router.put("/{ticket_id}", response_model=TicketResponse, summary="Editar chamado")
def update_ticket(
    ticket_id: int,
    dados: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")

    alteracoes = []
    for campo, valor in dados.model_dump(exclude_none=True).items():
        if getattr(ticket, campo) != valor:
            alteracoes.append(f"{campo}: {getattr(ticket, campo)} → {valor}")
            setattr(ticket, campo, valor)

    if alteracoes:
        _registrar_historico(
            db=db, ticket=ticket, usuario=current_user,
            tipo_acao=TipoAcao.EDICAO,
            comentario="Chamado editado: " + "; ".join(alteracoes)
        )

    db.commit()
    db.refresh(ticket)
    return ticket


# ============================================================
# ATUALIZAR STATUS
# ============================================================

@router.patch("/{ticket_id}/status", response_model=TicketResponse, summary="Alterar status")
def update_status(
    ticket_id: int,
    dados: TicketStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Altera o status do chamado e registra no histórico.
    Se status = RESOLVIDO ou FECHADO, registra data_fechamento.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")

    status_anterior = ticket.status
    nivel_anterior = ticket.nivel_atual

    if dados.status:
        ticket.status = dados.status
        if dados.status in [StatusChamado.RESOLVIDO, StatusChamado.FECHADO]:
            ticket.data_fechamento = datetime.utcnow()

    if dados.nivel_atual:
        ticket.nivel_atual = dados.nivel_atual

    _registrar_historico(
        db=db, ticket=ticket, usuario=current_user,
        tipo_acao=TipoAcao.MUDANCA_STATUS,
        comentario=dados.comentario,
        status_anterior=status_anterior,
        status_novo=dados.status,
        nivel_anterior=nivel_anterior,
        nivel_novo=dados.nivel_atual,
    )

    db.commit()
    db.refresh(ticket)
    return ticket


# ============================================================
# ENCAMINHAR CHAMADO ENTRE NÍVEIS (N1→N2→N3)
# ============================================================

@router.post("/{ticket_id}/encaminhar", response_model=TicketResponse, summary="Encaminhar chamado")
def encaminhar_ticket(
    ticket_id: int,
    dados: EncaminhamentoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Encaminha o chamado para outro nível de suporte.

    Regras do fluxo:
    - N1 pode encaminhar para N2
    - N2 pode encaminhar para N3 ou devolver para N1
    - N3 e ADMIN podem encaminhar para qualquer nível
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")

    nivel_anterior = ticket.nivel_atual
    ticket.nivel_atual = dados.nivel_destino

    # Ao encaminhar, o status volta para EM_ANALISE
    if ticket.status == StatusChamado.ABERTO:
        ticket.status = StatusChamado.EM_ANALISE

    _registrar_historico(
        db=db, ticket=ticket, usuario=current_user,
        tipo_acao=TipoAcao.ENCAMINHAMENTO,
        comentario=dados.comentario or f"Chamado encaminhado para {dados.nivel_destino.value}",
        nivel_anterior=nivel_anterior,
        nivel_novo=dados.nivel_destino,
    )

    db.commit()
    db.refresh(ticket)
    return ticket


# ============================================================
# ADICIONAR COMENTÁRIO
# ============================================================

@router.post("/{ticket_id}/comentarios", response_model=TicketResponse, summary="Adicionar comentário")
def add_comentario(
    ticket_id: int,
    dados: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")

    _registrar_historico(
        db=db, ticket=ticket, usuario=current_user,
        tipo_acao=TipoAcao.COMENTARIO,
        comentario=dados.comentario,
    )

    db.commit()
    db.refresh(ticket)
    return ticket


# ============================================================
# UPLOAD DE ANEXO
# ============================================================

@router.post("/{ticket_id}/anexos", status_code=201, summary="Upload de anexo")
async def upload_attachment(
    ticket_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Faz upload de um arquivo (imagem, PDF, etc.) para o chamado.
    O arquivo é salvo com nome UUID para evitar conflitos e sobrescrita.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")

    # Valida extensão
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=400,
            detail=f"Extensão '{ext}' não permitida. Permitidas: {settings.allowed_extensions}"
        )

    # Valida tamanho
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > settings.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"Arquivo muito grande. Máximo: {settings.max_file_size_mb}MB"
        )

    # Salva o arquivo com nome seguro (UUID)
    nome_seguro = f"{uuid.uuid4().hex}.{ext}"
    caminho = os.path.join(settings.upload_dir, str(ticket_id))
    os.makedirs(caminho, exist_ok=True)
    caminho_completo = os.path.join(caminho, nome_seguro)

    with open(caminho_completo, "wb") as f:
        f.write(content)

    # Registra no banco
    attachment = Attachment(
        ticket_id=ticket_id,
        usuario_id=current_user.id,
        nome_original=file.filename,
        nome_arquivo=nome_seguro,
        tipo_mime=file.content_type,
        tamanho_bytes=len(content),
        caminho=caminho_completo,
    )
    db.add(attachment)
    db.commit()

    return {"mensagem": "Arquivo enviado com sucesso.", "arquivo": file.filename}
