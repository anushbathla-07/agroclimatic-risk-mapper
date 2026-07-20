from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.core.db import Base

class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Stores the map boundary of the state
    boundary = Column(Geometry('POLYGON', srid=4326)) 
    
    districts = relationship("District", back_populates="state")

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    state_id = Column(Integer, ForeignKey("states.id"))
    
    # Stores the map boundary of the district
    boundary = Column(Geometry('POLYGON', srid=4326))
    
    state = relationship("State", back_populates="districts")
    villages = relationship("Village", back_populates="district")

class Village(Base):
    __tablename__ = "villages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"))
    
    # Stores the exact center point to focus the map camera
    center_point = Column(Geometry('POINT', srid=4326)) 
    
    district = relationship("District", back_populates="villages")