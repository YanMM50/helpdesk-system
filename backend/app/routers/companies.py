"""
routers/companies.py — CRUD de empresas e equipamentos
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company
from app.models.equipment import Equipment
from app.models.user import User
from app.schemas.company import (
    CompanyCreate, CompanyUpdate, CompanyResponse,
    EquipmentCreate, EquipmentUpdate, EquipmentResponse
)
from app.services.auth_service import get_current_user, require_admin

router = APIRouter(tags=["Empresas e Equipamentos"])


# ============================================================
# EMPRESAS
# ============================================================

@router.post("/companies", response_model=CompanyResponse, status_code=201)
def create_company(dados: CompanyCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    company = Company(**dados.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get("/companies", response_model=List[CompanyResponse])
def list_companies(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Company).filter(Company.ativo == True).all()


@router.get("/companies/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return company


@router.put("/companies/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, dados: CompanyUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(company, campo, valor)
    db.commit()
    db.refresh(company)
    return company


# ============================================================
# EQUIPAMENTOS
# ============================================================

@router.post("/equipments", response_model=EquipmentResponse, status_code=201)
def create_equipment(dados: EquipmentCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    equipment = Equipment(**dados.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


@router.get("/equipments", response_model=List[EquipmentResponse])
def list_equipments(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Equipment).filter(Equipment.ativo == True).all()


@router.get("/equipments/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(equipment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    eq = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado.")
    return eq


@router.put("/equipments/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(equipment_id: int, dados: EquipmentUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    eq = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado.")
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(eq, campo, valor)
    db.commit()
    db.refresh(eq)
    return eq
