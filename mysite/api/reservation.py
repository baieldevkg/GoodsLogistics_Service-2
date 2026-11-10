from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import InventoryReservation
from mysite.schemas.reservation_schema import (InventoryReservationInputSchema,
                                               InventoryReservationOutputSchema)
from mysite.database.db import SessionLocal

reservation_router = APIRouter(prefix='/reservation', tags=['Reservation Crud'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@reservation_router.post('/', response_model=InventoryReservationOutputSchema)
async def create_reservation(reservation: InventoryReservationInputSchema,
                             db: Session = Depends(get_db)):
    reservation_db = InventoryReservation(**reservation.model_dump())
    db.add(reservation_db)
    db.commit()
    db.refresh(reservation_db)
    return reservation_db


@reservation_router.get('/', response_model=List[InventoryReservationOutputSchema])
async def list_reservation(db: Session = Depends(get_db)):
    return db.query(InventoryReservation).all()


@reservation_router.get('/{reservation_id}/', response_model=InventoryReservationOutputSchema)
async def detail_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(InventoryReservation).filter(
        InventoryReservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(detail='Мындай брондоо жок', status_code=404)
    return reservation


@reservation_router.put('/{reservation_id}/', response_model=dict)
async def update_reservation(reservation_id: int, reservation: InventoryReservationInputSchema,
                             db: Session = Depends(get_db)):
    reservation_db = db.query(InventoryReservation).filter(
        InventoryReservation.id == reservation_id).first()
    if not reservation_db:
        raise HTTPException(detail='Мындай брондоо жок', status_code=404)

    for key, value in reservation.model_dump().items():
        setattr(reservation_db, key, value)

    db.commit()
    db.refresh(reservation_db)
    return {'message': 'Брондоо озгорулду'}


@reservation_router.delete('/{reservation_id}/', response_model=dict)
async def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation_db = db.query(InventoryReservation).filter(
        InventoryReservation.id == reservation_id).first()
    if not reservation_db:
        raise HTTPException(detail='Мындай брондоо жок', status_code=404)

    db.delete(reservation_db)
    db.commit()
    return {'message': 'Брондоо очту'}