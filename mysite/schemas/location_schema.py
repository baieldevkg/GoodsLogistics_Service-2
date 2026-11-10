from datetime import datetime
from pydantic import BaseModel


class CourierLocationInputSchema(BaseModel):
    courier_id: int
    latitude: float
    longitude: float


class CourierLocationOutputSchema(BaseModel):
    id: int
    courier_id: int
    latitude: float
    longitude: float
    recorded_at: datetime