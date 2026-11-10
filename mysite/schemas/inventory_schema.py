from datetime import datetime
from pydantic import BaseModel


class InventoryInputSchema(BaseModel):
    warehouse_id: int
    product_id: int
    quantity: int = 0
    reserved_quantity: int = 0


class InventoryOutputSchema(BaseModel):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    reserved_quantity: int
    updated_at: datetime