from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from database import get_db_context
from sqlalchemy.orm import Session
from starlette import status
from schemas.company import Company
from models.company import CompanyModel, CompanyViewModel

router = APIRouter(prefix="/company", tags=["Company"])


def http_exception():
    return HTTPException(status_code=404, detail="Item not found")


@router.get("", response_model=list[CompanyViewModel])
async def get_all_companies(db: Session = Depends(get_db_context)):
    return db.query(Company).all()


@router.get("/{company_id}")
async def get_company_by_id(company_id: UUID, db: Session = Depends(get_db_context)) -> CompanyViewModel:
    company = db.query(Company)\
        .filter(Company.id == company_id)\
        .first()
    if company is not None:
        return company
    raise http_exception()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_company(request: CompanyModel, db: Session = Depends(get_db_context)) -> None:
    company = Company(**request.dict())
    company.created_at = datetime.utcnow()

    db.add(company)
    db.commit()


@router.put("/{company_id}")
async def update_company(company_id: UUID, request: CompanyModel, db: Session = Depends(get_db_context)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise http_exception()
    company.full_name = request.full_name
    company.gender = request.gender
    company.updated_at = datetime.utcnow()

    db.add(company)
    db.commit()
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: UUID, db: Session = Depends(get_db_context)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise http_exception()

    db.delete(company)
    db.commit()
