from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import TrackingEvent
from mysite.schemas.tracking_schema import TrackingEventInputSchema, TrackingEventOutputSchema
from mysite.database.db import SessionLocal

tracking_router = APIRouter(prefix='/tracking', tags=['Tracking Crud'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@tracking_router.post('/', response_model=TrackingEventOutputSchema)
async def create_tracking(tracking: TrackingEventInputSchema, db: Session = Depends(get_db)):
    tracking_db = TrackingEvent(**tracking.model_dump())
    db.add(tracking_db)
    db.commit()
    db.refresh(tracking_db)
    return tracking_db


@tracking_router.get('/', response_model=List[TrackingEventOutputSchema])
async def list_tracking(db: Session = Depends(get_db)):
    return db.query(TrackingEvent).all()


@tracking_router.get('/{tracking_id}/', response_model=TrackingEventOutputSchema)
async def detail_tracking(tracking_id: int, db: Session = Depends(get_db)):
    tracking = db.query(TrackingEvent).filter(TrackingEvent.id == tracking_id).first()
    if not tracking:
        raise HTTPException(detail='Мындай трекинг жок', status_code=404)
    return tracking


@tracking_router.put('/{tracking_id}/', response_model=dict)
async def update_tracking(tracking_id: int, tracking: TrackingEventInputSchema,
                          db: Session = Depends(get_db)):
    tracking_db = db.query(TrackingEvent).filter(TrackingEvent.id == tracking_id).first()
    if not tracking_db:
        raise HTTPException(detail='Мындай трекинг жок', status_code=404)

    for key, value in tracking.model_dump().items():
        setattr(tracking_db, key, value)

    db.commit()
    db.refresh(tracking_db)
    return {'message': 'Трекинг озгорулду'}


@tracking_router.delete('/{tracking_id}/', response_model=dict)
async def delete_tracking(tracking_id: int, db: Session = Depends(get_db)):
    tracking_db = db.query(TrackingEvent).filter(TrackingEvent.id == tracking_id).first()
    if not tracking_db:
        raise HTTPException(detail='Мындай трекинг жок', status_code=404)

    db.delete(tracking_db)
    db.commit()
    return {'message': 'Трекинг очту'}