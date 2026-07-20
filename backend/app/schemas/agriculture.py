from pydantic import BaseModel

class CropCreate(BaseModel):
    name: str
    optimal_temp_min: float
    optimal_temp_max: float
    required_rainfall_mm: float

class CropResponse(CropCreate):
    id: int

    class Config:
        from_attributes = True