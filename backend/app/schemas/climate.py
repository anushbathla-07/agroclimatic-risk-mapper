from pydantic import BaseModel
from datetime import date

class ClimateCreate(BaseModel):
    district_name: str
    record_date: date
    temperature_min: float
    temperature_max: float
    rainfall_mm: float

class ClimateResponse(ClimateCreate):
    id: int

    class Config:
        from_attributes = True # Replaces orm_mode=True in newer Pydantic versions