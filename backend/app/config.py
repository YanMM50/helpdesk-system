"""
config.py — Configurações centrais da aplicação

Usa pydantic-settings para ler as variáveis do arquivo .env
automaticamente. Centralizar as configs aqui evita valores
espalhados pelo código ("magic strings").
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Banco de dados
    database_url: str = "postgresql://postgres:postgres@localhost:5432/helpdesk_db"

    # JWT
    secret_key: str = "CHAVE_INSEGURA_TROQUE_NO_ENV"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480

    # Servidor
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # Upload
    upload_dir: str = "uploads"
    max_file_size_mb: int = 10
    allowed_extensions: str = "jpg,jpeg,png,gif,pdf,txt,doc,docx"

    # Supabase Storage
    supabase_url: str = ""
    supabase_service_key: str = ""
    supabase_bucket: str = "tickets"

    # App
    app_name: str = "Help Desk System"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def allowed_extensions_list(self) -> list[str]:
        return [ext.strip() for ext in self.allowed_extensions.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna a instância das configurações.
    @lru_cache garante que o arquivo .env é lido apenas uma vez.
    """
    return Settings()
