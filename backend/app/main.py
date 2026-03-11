"""
main.py — Ponto de entrada da aplicação FastAPI

Este arquivo:
1. Cria a instância do FastAPI
2. Configura CORS (para o frontend poder chamar a API)
3. Registra todos os roteadores
4. Serve arquivos estáticos (uploads)
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, users, companies, tickets, dashboard

# Importa os models para que o SQLAlchemy os reconheça ao criar tabelas
import app.models  # noqa: F401

settings = get_settings()

# =============================================================
# Instância principal do FastAPI
# =============================================================
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## Sistema de Gestão de Chamados Técnicos (Help Desk)

    API REST para gerenciamento de incidentes e solicitações técnicas
    com suporte em três níveis (N1, N2, N3).

    ### Funcionalidades:
    - Autenticação JWT
    - Gestão de chamados com fluxo N1 → N2 → N3
    - Histórico completo de atendimento
    - Upload de evidências (fotos/arquivos)
    - Dashboard com estatísticas
    - Gestão de empresas e equipamentos
    """,
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc (documentação alternativa)
)

# =============================================================
# CORS — permite que o frontend HTML acesse a API
# Em produção, substitua "*" pelo domínio real do frontend
# =============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Em produção: ["https://seudominio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================
# Criação das tabelas no banco (se não existirem)
# Em produção, use migrações com Alembic em vez disso
# =============================================================
Base.metadata.create_all(bind=engine)

# =============================================================
# Registro dos roteadores
# Cada roteador agrupa endpoints relacionados
# =============================================================
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(tickets.router)
app.include_router(dashboard.router)

# =============================================================
# Servir arquivos de upload como estáticos
# =============================================================
upload_dir = settings.upload_dir
os.makedirs(upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")


# =============================================================
# Endpoint de saúde (health check)
# =============================================================
@app.get("/", tags=["Sistema"])
def root():
    """Verifica se a API está online."""
    return {
        "sistema": settings.app_name,
        "versao": settings.app_version,
        "status": "online",
        "documentacao": "/docs",
    }


@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "healthy"}
