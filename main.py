import uvicorn
from fastapi import FastAPI
from mysite.database.db import Base, engine
from mysite.database import models
from mysite.api import warehouse, inventory, reservation, courier, location, delivery, route, stop, tracking

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Goods Logistics')

app.include_router(warehouse.warehouse_router)
app.include_router(inventory.inventory_router)
app.include_router(reservation.reservation_router)
app.include_router(courier.courier_router)
app.include_router(location.location_router)
app.include_router(delivery.delivery_router)
app.include_router(route.route_router)
app.include_router(stop.stop_router)
app.include_router(tracking.tracking_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8005)