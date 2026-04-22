"""
routers/dashboard.py — Estatísticas para o painel principal
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ticket import Ticket, StatusChamado, PrioridadeChamado
from app.models.user import User, NivelSuporte
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/resumo", summary="Resumo geral para o dashboard")
def get_resumo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna contadores e agrupamentos para montar o dashboard.
    Todas as queries são feitas em uma única chamada para performance.
    """
    base = db.query(Ticket)

    # Total por status
    por_status = (
        db.query(Ticket.status, func.count(Ticket.id).label("total"))
        .group_by(Ticket.status)
        .all()
    )

    # Total por prioridade (apenas abertos)
    por_prioridade = (
        db.query(Ticket.prioridade, func.count(Ticket.id).label("total"))
        .filter(Ticket.status.notin_([StatusChamado.RESOLVIDO, StatusChamado.FECHADO]))
        .group_by(Ticket.prioridade)
        .all()
    )

    # Total por nível de suporte (apenas abertos)
    por_nivel = (
        db.query(Ticket.nivel_atual, func.count(Ticket.id).label("total"))
        .filter(Ticket.status.notin_([StatusChamado.RESOLVIDO, StatusChamado.FECHADO]))
        .group_by(Ticket.nivel_atual)
        .all()
    )

    # Chamados abertos (não fechados/resolvidos)
    total_abertos = base.filter(
        Ticket.status.notin_([StatusChamado.RESOLVIDO, StatusChamado.FECHADO])
    ).count()

    # Chamados críticos abertos
    total_criticos = base.filter(
        Ticket.prioridade == PrioridadeChamado.CRITICA,
        Ticket.status.notin_([StatusChamado.RESOLVIDO, StatusChamado.FECHADO])
    ).count()

    # Últimos 5 chamados abertos
    ultimos = (
        base.filter(Ticket.status == StatusChamado.ABERTO)
        .order_by(Ticket.data_abertura.desc())
        .limit(5)
        .all()
    )

    # Chamados com SLA vencido (prazo passou, status ainda aberto)
    agora = datetime.utcnow()
    total_vencidos = base.filter(
        Ticket.prazo_sla < agora,
        Ticket.status.notin_([StatusChamado.RESOLVIDO, StatusChamado.FECHADO]),
        Ticket.prazo_sla.isnot(None),
    ).count()

    # Tempo médio de resolução em horas
    fechados = (
        db.query(Ticket.data_abertura, Ticket.data_fechamento)
        .filter(
            Ticket.status.in_([StatusChamado.RESOLVIDO, StatusChamado.FECHADO]),
            Ticket.data_fechamento.isnot(None),
            Ticket.data_abertura.isnot(None),
        )
        .all()
    )
    if fechados:
        total_horas = sum(
            (t.data_fechamento - t.data_abertura).total_seconds() / 3600
            for t in fechados
            if t.data_fechamento > t.data_abertura
        )
        tempo_medio_resolucao = round(total_horas / len(fechados), 1)
    else:
        tempo_medio_resolucao = None

    return {
        "total_abertos": total_abertos,
        "total_criticos": total_criticos,
        "total_vencidos": total_vencidos,
        "tempo_medio_resolucao": tempo_medio_resolucao,
        "por_status": {row.status.value: row.total for row in por_status},
        "por_prioridade": {row.prioridade.value: row.total for row in por_prioridade},
        "por_nivel": {row.nivel_atual.value: row.total for row in por_nivel},
        "ultimos_chamados": [
            {
                "id": t.id,
                "protocolo": t.protocolo,
                "titulo": t.titulo,
                "prioridade": t.prioridade.value,
                "status": t.status.value,
                "nivel_atual": t.nivel_atual.value,
                "data_abertura": t.data_abertura.isoformat() if t.data_abertura else None,
                "prazo_sla": t.prazo_sla.isoformat() if t.prazo_sla else None,
            }
            for t in ultimos
        ]
    }
