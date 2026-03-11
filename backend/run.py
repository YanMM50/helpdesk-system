"""
run.py — Script para iniciar o servidor de desenvolvimento

Como usar:
    python run.py

Ou diretamente com uvicorn:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
import uvicorn
from app.config import get_settings

settings = get_settings()

if __name__ == "__main__":
    print(f"🚀 Iniciando {settings.app_name} v{settings.app_version}")
    print(f"📖 Documentação: http://localhost:{settings.port}/docs")
    print(f"🔧 Modo debug: {settings.debug}")

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,  # Hot reload em desenvolvimento
        log_level="info",
    )
