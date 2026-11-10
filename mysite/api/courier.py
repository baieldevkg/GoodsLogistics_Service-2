from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Courier
from mysite.schemas.courier_schema import CourierInputSchema, CourierOutputSchema
from mysite.database.db import SessionLocal

courier_router = APIRouter(prefix='/courier', tags=['Courier Crud'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@courier_router.post('/', response_model=CourierOutputSchema)
async def create_courier(courier: CourierInputSchema, db: Session = Depends(get_db)):
    courier_db = Courier(**courier.model_dump())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@courier_router.get('/', response_model=List[CourierOutputSchema])
async def list_courier(db: Session = Depends(get_db)):
    return db.query(Courier).all()


@courier_router.get('/{courier_id}/', response_model=CourierOutputSchema)
async def detail_courier(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier:
        raise HTTPException(detail='Мындай курьер жок', status_code=404)
    return courier


@courier_router.put('/{courier_id}/', response_model=dict)
async def update_courier(courier_id: int, courier: CourierInputSchema,
                         db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='Мындай курьер жок', status_code=404)

    for key, value in courier.model_dump().items():
        setattr(courier_db, key, value)

    db.commit()
    db.refresh(courier_db)
    return {'message': 'Курьер озгорулду'}


@courier_router.delete('/{courier_id}/', response_model=dict)
async def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='Мындай курьер жок', status_code=404)

    db.delete(courier_db)
    db.commit()
    return {'message': 'Курьер очту'}