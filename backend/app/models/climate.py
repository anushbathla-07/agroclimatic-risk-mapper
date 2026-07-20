from sqlalchemy import Column, Integer, String, Float, Date
from app.core.db import Base

class Climate(Base):
    __tablename__ = "climate_data"

    id = Column(Integer, primary_key=True, index=True)
    district_name = Column(String, index=True, comment="e.g., Meerut")
    record_date = Column(Date, index=True, comment="The date this weather was recorded")
    
    # Core weather metrics
    temperature_min = Column(Float, comment="Recorded minimum temperature in Celsius")
    temperature_max = Column(Float, comment="Recorded maximum temperature in Celsius")
    rainfall_mm = Column(Float, comment="Recorded rainfall in mm")