from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import CourierLocation
from mysite.schemas.location_schema import CourierLocationInputSchema, CourierLocationOutputSchema
from mysite.database.db import SessionLocal

location_router = APIRouter(prefix='/location', tags=['Location Crud'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@location_router.post('/', response_model=CourierLocationOutputSchema)
async def create_location(location: CourierLocationInputSchema, db: Session = Depends(get_db)):
    location_db = CourierLocation(**location.model_dump())
    db.add(location_db)
    db.commit()
    db.refresh(location_db)
    return location_db


@location_router.get('/', response_model=List[CourierLocationOutputSchema])
async def list_location(db: Session = Depends(get_db)):
    return db.query(CourierLocation).all()


@location_router.get('/{location_id}/', response_model=CourierLocationOutputSchema)
async def detail_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(CourierLocation).filter(CourierLocation.id == location_id).first()
    if not location:
        raise HTTPException(detail='Мындай локация жок', status_code=404)
    return location


@location_router.put('/{location_id}/', response_model=dict)
async def update_location(location_id: int, location: CourierLocationInputSchema,
                          db: Session = Depends(get_db)):
    location_db = db.query(CourierLocation).filter(CourierLocation.id == location_id).first()
    if not location_db:
        raise HTTPException(detail='Мындай локация жок', status_code=404)

    for key, value in location.model_dump().items():
        setattr(location_db, key, value)

    db.commit()
    db.refresh(location_db)
    return {'message': 'Локация озгорулду'}


@location_router.delete('/{location_id}/', response_model=dict)
async def delete_location(location_id: int, db: Session = Depends(get_db)):
    location_db = db.query(CourierLocation).filter(CourierLocation.id == location_id).first()
    if not location_db:
        raise HTTPException(detail='Мындай локация жок', status_code=404)

    db.delete(location_db)
    db.commit()
    return {'message': 'Локация очту'}