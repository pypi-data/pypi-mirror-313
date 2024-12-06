from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from .series_abstract import SerieAbstract
from sqlalchemy.orm import relationship
from .areas import Area

class SerieAreal(SerieAbstract):
    __tablename__ = 'series_areal'
    
    area_id = Column(Integer, ForeignKey('areas_pluvio.unid', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    fuentes_id = Column(Integer, nullable=False)

    area = relationship("Area",back_populates="series_areal") # , backref="series_areal")

    __table_args__ = (UniqueConstraint('fuentes_id', 'proc_id', 'unit_id', 'var_id', 'area_id', name = 'series_areal_fuentes_id_proc_id_unit_id_var_id_area_id_key'),)

    def __repr__(self):
        return f"<SerieAreal(id={self.id}, nombre={self.nombre}, area_id={self.area_id}, fuentes_id={self.fuentes_id})>"
