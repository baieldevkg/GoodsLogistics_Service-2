from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from mysite.database.models import TransportType, CourierStatus


class CourierInputSchema(BaseModel):
    warehouse_id: int
    transport_type: TransportType
    status: CourierStatus = CourierStatus.offline
    max_active_orders: int = Field(default=3, ge=1, le=20)


class CourierUpdateSchema(BaseModel):
    warehouse_id: Optional[int] = None
    transport_type: Optional[TransportType] = None
    status: Optional[CourierStatus] = None
    max_active_orders: Optional[int] = Field(default=None, ge=1, le=20)


class CourierOutputSchema(BaseModel):
    id: int
    user_id: int
    warehouse_id: int
    transport_type: TransportType
    status: CourierStatus
    max_active_orders: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CourierCreateSchema(BaseModel):
    warehouse_id: int
    transport_type: TransportType
    status: CourierStatus = CourierStatus.offline
    max_active_orders: int = Field(default=3, ge=1, le=20)