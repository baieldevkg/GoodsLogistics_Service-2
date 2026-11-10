from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from mysite.database.models import StopType, StopStatus


class RouteStopInputSchema(BaseModel):
    route_id: int
    delivery_id: int
    stop_type: StopType
    sequence: int
    latitude: float
    longitude: float
    status: StopStatus = StopStatus.pending
    arrived_at: Optional[datetime] = None


class RouteStopOutputSchema(BaseModel):
    id: int
    route_id: int
    delivery_id: int
    stop_type: StopType
    sequence: int
    latitude: float
    longitude: float
    status: StopStatus
    arrived_at: Optional[datetime]