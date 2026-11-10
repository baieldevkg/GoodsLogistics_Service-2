from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Warehouse
from mysite.schemas.warehouse_schema import WarehouseInputSchema, WarehouseOutputSchema
from mysite.database.db import SessionLocal

warehouse_router = APIRouter(prefix='/warehouse', tags=['Warehouse Crud'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@warehouse_router.post('/', response_model=WarehouseOutputSchema)
async def create_warehouse(warehouse: WarehouseInputSchema, db: Session = Depends(get_db)):
    warehouse_db = Warehouse(**warehouse.model_dump())
    db.add(warehouse_db)
    db.commit()
    db.refresh(warehouse_db)
    return warehouse_db


@warehouse_router.get('/', response_model=List[WarehouseOutputSchema])
async def list_warehouse(db: Session = Depends(get_db)):
    return db.query(Warehouse).all()


@warehouse_router.get('/{warehouse_id}/', response_model=WarehouseOutputSchema)
async def detail_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(detail='Мындай склад жок', status_code=404)
    return warehouse


@warehouse_router.put('/{warehouse_id}/', response_model=dict)
async def update_warehouse(warehouse_id: int, warehouse: WarehouseInputSchema,
                           db: Session = Depends(get_db)):
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(detail='Мындай склад жок', status_code=404)

    for key, value in warehouse.model_dump().items():
        setattr(warehouse_db, key, value)

    db.commit()
    db.refresh(warehouse_db)
    return {'message': 'Склад озгорулду'}


@warehouse_router.delete('/{warehouse_id}/', response_model=dict)
async def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(detail='Мындай склад жок', status_code=404)

    db.delete(warehouse_db)
    db.commit()
    return {'message': 'Склад очту'}