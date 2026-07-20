from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import joblib
import warnings

# Database and Model imports
from app.core.db import engine, Base, SessionLocal
from app.models import agriculture
from app.models import location
from app.models import climate
from app.api import locations

# Schema and Model for the specific route
from app.models.agriculture import Crop
from app.schemas.agriculture import CropCreate, CropResponse
from app.models.climate import Climate
from app.schemas.climate import ClimateCreate, ClimateResponse

# Suppress scikit-learn version warnings for cleaner terminal output
warnings.filterwarnings("ignore", category=UserWarning)

# Yeh line Supabase/PostgreSQL mein tables create karegi (agar wo pehle se nahi hain)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Skipping table auto-creation with spatial warning: {e}")

app = FastAPI(title="AgroClimatic Risk Mapper API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# LOAD THE MACHINE LEARNING MODEL (The "Brain")
# ---------------------------------------------------------
try:
    rf_model = joblib.load("saved_models/random_forest_risk_model.pkl")
    label_encoder = joblib.load("saved_models/crop_label_encoder.pkl")
    print("✅ AI Model Loaded Successfully!")
except Exception as e:
    print(f"⚠️ Warning: Could not load ML model. Error: {e}")

# Existing Location Routes
app.include_router(locations.router, prefix="/api/v1/locations", tags=["Locations"])

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Default Route
@app.get("/")
def read_root():
    return {"status": "success", "message": "AgroClimatic API is running live!"}

# ---------------------------------------------------------
# AGRICULTURE & CLIMATE ROUTES (Kept the same)
# ---------------------------------------------------------

@app.post("/api/v1/crops", response_model=CropResponse, tags=["Agriculture"])
def create_crop(crop: CropCreate, db: Session = Depends(get_db)):
    new_crop = Crop(**crop.model_dump()) 
    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)
    return new_crop

@app.get("/api/v1/crops", response_model=List[CropResponse], tags=["Agriculture"])
def get_all_crops(db: Session = Depends(get_db)):
    return db.query(Crop).all()

@app.post("/api/v1/climate", response_model=ClimateResponse, tags=["Climate"])
def create_climate_record(climate_data: ClimateCreate, db: Session = Depends(get_db)):
    new_record = Climate(**climate_data.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@app.get("/api/v1/climate", response_model=List[ClimateResponse], tags=["Climate"])
def get_all_climate_records(db: Session = Depends(get_db)):
    return db.query(Climate).all()

# ---------------------------------------------------------
# NEW AI-POWERED ANALYTICS ROUTE
# ---------------------------------------------------------

@app.get("/api/v1/risk-assessment", tags=["Analytics"])
def calculate_risk(district: str, crop_name: str, db: Session = Depends(get_db)):
    # 1. Fetch the crop and climate data from PostgreSQL
    crop = db.query(Crop).filter(Crop.name.ilike(crop_name)).first()
    if not crop:
        raise HTTPException(status_code=404, detail=f"Crop '{crop_name}' not found.")

    climate = db.query(Climate).filter(Climate.district_name.ilike(district)).order_by(Climate.id.desc()).first()
    if not climate:
        raise HTTPException(status_code=404, detail=f"No climate data found for '{district}'.")

    # 2. Prepare the data for the AI Model
    try:
        # Encode the text crop name into the number the AI expects
        encoded_crop = label_encoder.transform([crop.name])[0]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"AI Model has not been trained on crop: {crop.name}")
    
    # Create the feature array [Crop, Max Temp, Min Temp, Rainfall]
    features = [[encoded_crop, climate.temperature_max, climate.temperature_min, climate.rainfall_mm]]

    # 3. Ask the AI Model to predict the risk!
    prediction = rf_model.predict(features)[0]
    
    # Map the AI prediction to a score and message for the Streamlit dashboard
    if prediction == "High":
        risk_score = 8
        ai_warning = f"AI Prediction: High risk of crop failure due to extreme weather patterns."
    elif prediction == "Moderate":
        risk_score = 5
        ai_warning = f"AI Prediction: Moderate stress detected. Monitoring recommended."
    else:
        risk_score = 1
        ai_warning = f"AI Prediction: Low risk. Conditions are favorable."

    return {
        "district": district,
        "crop": crop.name,
        "overall_risk_level": prediction,
        "risk_score_out_of_10": risk_score,
        "warnings": [ai_warning],
        "data_used": {
            "recorded_max_temp": climate.temperature_max,
            "recorded_rainfall": climate.rainfall_mm
        }
    }