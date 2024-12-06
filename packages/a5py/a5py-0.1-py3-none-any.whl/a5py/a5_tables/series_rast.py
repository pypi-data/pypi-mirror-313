from sqlalchemy import Column, Integer, String
from .series_abstract import SerieAbstract

class SerieRast(SerieAbstract):
    __tablename__ = 'series_rast'
    
    escena_id = Column(Integer)
    fuentes_id = Column(Integer)

    def __repr__(self):
        return f"<SerieRast(id={self.id}, nombre={self.nombre})>"
