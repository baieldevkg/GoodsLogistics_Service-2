from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Delivery
from mysite.schemas.delivery_schema import DeliveryInputSchema, DeliveryOutputSchema
from mysite.database.db import SessionLocal

delivery_router = APIRouter(prefix='/delivery', tags=['Delivery Crud'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@delivery_router.post('/', response_model=DeliveryOutputSchema)
async def create_delivery(delivery: DeliveryInputSchema, db: Session = Depends(get_db)):
    delivery_db = Delivery(**delivery.model_dump())
    db.add(delivery_db)
    db.commit()
    db.refresh(delivery_db)
    return delivery_db


@delivery_router.get('/', response_model=List[DeliveryOutputSchema])
async def list_delivery(db: Session = Depends(get_db)):
    return db.query(Delivery).all()


@delivery_router.get('/{delivery_id}/', response_model=DeliveryOutputSchema)
async def detail_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(detail='Мындай жеткирүү жок', status_code=404)
    return delivery


@delivery_router.put('/{delivery_id}/', response_model=dict)
async def update_delivery(delivery_id: int, delivery: DeliveryInputSchema,
                          db: Session = Depends(get_db)):
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(detail='Мындай жеткирүү жок', status_code=404)

    for key, value in delivery.model_dump().items():
        setattr(delivery_db, key, value)

    db.commit()
    db.refresh(delivery_db)
    return {'message': 'Жеткирүү озгорулду'}


@delivery_router.delete('/{delivery_id}/', response_model=dict)
async def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(detail='Мындай жеткирүү жок', status_code=404)

    db.delete(delivery_db)
    db.commit()
    return {'message': 'Жеткирүү очту'}