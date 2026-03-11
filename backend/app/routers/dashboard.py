"""
routers/dashboard.py — Estatísticas para o painel principal
"""
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

    return {
        "total_abertos": total_abertos,
        "total_criticos": total_criticos,
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
            }
            for t in ultimos
        ]
    }
