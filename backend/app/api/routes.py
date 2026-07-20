from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.agriculture import Crop
from app.schemas.agriculture import CropCreate, CropResponse
from app.core.db import SessionLocal

# If adding directly to main.py, use @app.post instead of @router.post
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/v1/crops", response_model=CropResponse)
def create_crop(crop: CropCreate, db: Session = Depends(get_db)):
    new_crop = Crop(**crop.model_dump()) # Use crop.dict() if on an older Pydantic version
    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)
    return new_crop