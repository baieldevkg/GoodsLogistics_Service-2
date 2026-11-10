from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import RouteStop
from mysite.schemas.stop_schema import RouteStopInputSchema, RouteStopOutputSchema
from mysite.database.db import SessionLocal

stop_router = APIRouter(prefix='/stop', tags=['Stop Crud'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@stop_router.post('/', response_model=RouteStopOutputSchema)
async def create_stop(stop: RouteStopInputSchema, db: Session = Depends(get_db)):
    stop_db = RouteStop(**stop.model_dump())
    db.add(stop_db)
    db.commit()
    db.refresh(stop_db)
    return stop_db


@stop_router.get('/', response_model=List[RouteStopOutputSchema])
async def list_stop(db: Session = Depends(get_db)):
    return db.query(RouteStop).all()


@stop_router.get('/{stop_id}/', response_model=RouteStopOutputSchema)
async def detail_stop(stop_id: int, db: Session = Depends(get_db)):
    stop = db.query(RouteStop).filter(RouteStop.id == stop_id).first()
    if not stop:
        raise HTTPException(detail='Мындай токтоочу жай жок', status_code=404)
    return stop


@stop_router.put('/{stop_id}/', response_model=dict)
async def update_stop(stop_id: int, stop: RouteStopInputSchema,
                      db: Session = Depends(get_db)):
    stop_db = db.query(RouteStop).filter(RouteStop.id == stop_id).first()
    if not stop_db:
        raise HTTPException(detail='Мындай токтоочу жай жок', status_code=404)

    for key, value in stop.model_dump().items():
        setattr(stop_db, key, value)

    db.commit()
    db.refresh(stop_db)
    return {'message': 'Токтоочу жай озгорулду'}


@stop_router.delete('/{stop_id}/', response_model=dict)
async def delete_stop(stop_id: int, db: Session = Depends(get_db)):
    stop_db = db.query(RouteStop).filter(RouteStop.id == stop_id).first()
    if not stop_db:
        raise HTTPException(detail='Мындай токтоочу жай жок', status_code=404)

    db.delete(stop_db)
    db.commit()
    return {'message': 'Токтоочу жай очту'}