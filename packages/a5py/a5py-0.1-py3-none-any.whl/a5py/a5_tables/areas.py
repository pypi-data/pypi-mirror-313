from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Sequence
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from geoalchemy2 import Geometry

from .base import Base
from .a5_base import A5Base
from .a5_types.raster import Raster

class Area(Base, A5Base):
    __tablename__ = 'areas_pluvio'
    
    id = Column(
        'unid',
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    geom = Column(Geometry('POLYGON', srid=4326), nullable=False)  # Polygon geometry with SRID 4326
    exutorio = Column(Geometry('POINT', srid=4326))  # Point geometry with SRID 4326
    nombre = Column(String(64))  # Variable character with max length 64
    area = Column(DOUBLE_PRECISION, default=0.0)  # Double precision, default 0
    rho = Column(Float, default=0.5)  # Real type, default 0.5
    ae = Column(Float, default=1.0)  # Real type, default 1
    wp = Column(Float, default=0.03)  # Real type, default 0.03
    uru_index = Column(Integer)  # Integer type
    activar = Column(Boolean, default=True)  # Boolean, default True
    as_max = Column(Float)  # Real type
    rast = Column(Raster)  
    mostrar = Column(Boolean, default=True)  #

    series_areal = relationship("SerieAreal", back_populates="area", cascade="all, delete-orphan")
