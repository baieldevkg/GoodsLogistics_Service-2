from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Route
from mysite.schemas.route_schema import RouteInputSchema, RouteOutputSchema
from mysite.database.db import SessionLocal

route_router = APIRouter(prefix='/route', tags=['Route Crud'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@route_router.post('/', response_model=RouteOutputSchema)
async def create_route(route: RouteInputSchema, db: Session = Depends(get_db)):
    route_db = Route(**route.model_dump())
    db.add(route_db)
    db.commit()
    db.refresh(route_db)
    return route_db


@route_router.get('/', response_model=List[RouteOutputSchema])
async def list_route(db: Session = Depends(get_db)):
    return db.query(Route).all()


@route_router.get('/{route_id}/', response_model=RouteOutputSchema)
async def detail_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(detail='Мындай маршрут жок', status_code=404)
    return route


@route_router.put('/{route_id}/', response_model=dict)
async def update_route(route_id: int, route: RouteInputSchema,
                       db: Session = Depends(get_db)):
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(detail='Мындай маршрут жок', status_code=404)

    for key, value in route.model_dump().items():
        setattr(route_db, key, value)

    db.commit()
    db.refresh(route_db)
    return {'message': 'Маршрут озгорулду'}


@route_router.delete('/{route_id}/', response_model=dict)
async def delete_route(route_id: int, db: Session = Depends(get_db)):
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(detail='Мындай маршрут жок', status_code=404)

    db.delete(route_db)
    db.commit()
    return {'message': 'Маршрут очту'}