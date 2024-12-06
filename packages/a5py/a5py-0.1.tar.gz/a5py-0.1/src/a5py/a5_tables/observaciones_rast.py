from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .a5_types.raster import Raster
from .series_rast import SerieRast
from .observaciones_abstract import ObservacionAbstract

class ObservacionRast(ObservacionAbstract):
    __tablename__ = 'observaciones_rast'
    
    # Define columns
    series_id = Column(Integer, ForeignKey('series_rast.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    valor = Column(Raster, nullable=False)  # Raster data stored as binary

    # Define relationship to the 'series_rast' table (assuming SerieRast is already defined)
    series = relationship("SerieRast", backref="observaciones_rast")

    # Unique constraint on (series_id, timestart, timeend)
    __table_args__ = (
        UniqueConstraint('series_id', 'timestart', 'timeend', name='observaciones_rast_series_id_timestart_timeend_key'),
    )
    
    def __repr__(self):
        return f"<ObservacionRast(id={self.id}, series_id={self.series_id}, timestart={self.timestart}, timeend={self.timeend}, validada={self.validada})>"
