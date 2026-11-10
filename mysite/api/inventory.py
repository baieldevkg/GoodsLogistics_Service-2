from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Inventory
from mysite.schemas.inventory_schema import InventoryInputSchema, InventoryOutputSchema
from mysite.database.db import SessionLocal

inventory_router = APIRouter(prefix='/inventory', tags=['Inventory Crud'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@inventory_router.post('/', response_model=InventoryOutputSchema)
async def create_inventory(inventory: InventoryInputSchema, db: Session = Depends(get_db)):
    inventory_db = Inventory(**inventory.model_dump())
    db.add(inventory_db)
    db.commit()
    db.refresh(inventory_db)
    return inventory_db


@inventory_router.get('/', response_model=List[InventoryOutputSchema])
async def list_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()


@inventory_router.get('/{inventory_id}/', response_model=InventoryOutputSchema)
async def detail_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(detail='Мындай инвентарь жок', status_code=404)
    return inventory


@inventory_router.put('/{inventory_id}/', response_model=dict)
async def update_inventory(inventory_id: int, inventory: InventoryInputSchema,
                           db: Session = Depends(get_db)):
    inventory_db = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_db:
        raise HTTPException(detail='Мындай инвентарь жок', status_code=404)

    for key, value in inventory.model_dump().items():
        setattr(inventory_db, key, value)

    db.commit()
    db.refresh(inventory_db)
    return {'message': 'Инвентарь озгорулду'}


@inventory_router.delete('/{inventory_id}/', response_model=dict)
async def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory_db = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_db:
        raise HTTPException(detail='Мындай инвентарь жок', status_code=404)

    db.delete(inventory_db)
    db.commit()
    return {'message': 'Инвентарь очту'}