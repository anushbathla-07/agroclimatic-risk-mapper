from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.location import State, District

router = APIRouter()

@router.get("/states")
def get_states(db: Session = Depends(get_db)):
    # Database se saari states fetch karna
    states = db.query(State).all()
    return states

@router.get("/districts")
def get_districts(state_id: int, db: Session = Depends(get_db)):
    # Database se specific state ke districts fetch karna
    districts = db.query(District).filter(District.state_id == state_id).all()
    return districts