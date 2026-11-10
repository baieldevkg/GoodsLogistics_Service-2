from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from mysite.database.models import RouteStatus


class RouteInputSchema(BaseModel):
    courier_id: int
    status: RouteStatus = RouteStatus.planned
    total_distance_km: float
    estimated_duration_min: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class RouteOutputSchema(BaseModel):
    id: int
    courier_id: int
    status: RouteStatus
    total_distance_km: float
    estimated_duration_min: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime