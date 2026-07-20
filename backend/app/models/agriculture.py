from sqlalchemy import Column, Integer, String, Float, ForeignKey
from geoalchemy2 import Geometry
from app.core.db import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Changed 'help' to 'comment' to fix the SQLAlchemy TypeError
    optimal_temp_min = Column(Float, comment="Minimum optimal temperature in Celsius")
    optimal_temp_max = Column(Float, comment="Maximum optimal temperature in Celsius")
    required_rainfall_mm = Column(Float, comment="Required rainfall in mm per season")

class FarmPlot(Base):
    __tablename__ = "farm_plots"

    id = Column(Integer, primary_key=True, index=True)
    district_name = Column(String, index=True) 
    
    boundaries = Column(Geometry('POLYGON', srid=4326)) 
    
    crop_id = Column(Integer, ForeignKey("crops.id"))