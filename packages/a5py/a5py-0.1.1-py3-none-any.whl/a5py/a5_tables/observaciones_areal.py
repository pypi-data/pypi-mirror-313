from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .series_areal import SerieAreal
from .observaciones_abstract import ObservacionAbstract

class ObservacionAreal(ObservacionAbstract):
    __tablename__ = 'observaciones_areal'
    
    # Define columns
    series_id = Column(Integer, ForeignKey('series_areal.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    valor = Column(Float, nullable=False)  # Raster data stored as binary

    series = relationship("SerieAreal", backref="observaciones_areal")

    # Unique constraint on (series_id, timestart, timeend)
    __table_args__ = (
        UniqueConstraint('series_id', 'timestart', 'timeend', name='observaciones_areal_series_id_timestart_timeend_key'),
    )
    
    def __repr__(self):
        return f"<ObservacionAreal(id={self.id}, series_id={self.series_id}, timestart={self.timestart}, timeend={self.timeend}, validada={self.validada})>"
