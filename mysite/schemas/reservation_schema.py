from datetime import datetime
from pydantic import BaseModel
from mysite.database.models import ReservationStatus


class InventoryReservationInputSchema(BaseModel):
    order_id: int
    inventory_id: int
    quantity: int
    status: ReservationStatus = ReservationStatus.active
    expires_at: datetime


class InventoryReservationOutputSchema(BaseModel):
    id: int
    order_id: int
    inventory_id: int
    quantity: int
    status: ReservationStatus
    expires_at: datetime
    created_at: datetime