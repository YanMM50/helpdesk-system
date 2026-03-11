"""
schemas/company.py — Formatos de entrada e saída para empresas e equipamentos
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CompanyCreate(BaseModel):
    nome: str
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None


class CompanyUpdate(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None


class CompanyResponse(BaseModel):
    id: int
    nome: str
    cnpj: Optional[str]
    telefone: Optional[str]
    email: Optional[str]
    endereco: Optional[str]
    ativo: bool
    criado_em: datetime

    model_config = {"from_attributes": True}


class EquipmentCreate(BaseModel):
    nome: str
    tipo: Optional[str] = None
    fabricante: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    patrimonio: Optional[str] = None
    company_id: Optional[int] = None
    responsavel_id: Optional[int] = None


class EquipmentUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    fabricante: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    patrimonio: Optional[str] = None
    company_id: Optional[int] = None
    responsavel_id: Optional[int] = None
    ativo: Optional[bool] = None


class EquipmentResponse(BaseModel):
    id: int
    nome: str
    tipo: Optional[str]
    fabricante: Optional[str]
    modelo: Optional[str]
    numero_serie: Optional[str]
    patrimonio: Optional[str]
    company_id: Optional[int]
    responsavel_id: Optional[int]
    ativo: bool
    criado_em: datetime

    model_config = {"from_attributes": True}
