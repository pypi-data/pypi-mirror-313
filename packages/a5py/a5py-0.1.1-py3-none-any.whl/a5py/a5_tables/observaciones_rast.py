from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import os
from datetime import datetime
from typing import Union

from .a5_types.raster import Raster
from .series_rast import SerieRast
from .observaciones_abstract import ObservacionAbstract

from ..util import importRaster, upsertObservacionRaster, is_text_file, validate_date

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

    @classmethod
    def load(cls, connection, input_filename : str,timestart : Union[datetime,str], series_id : int, **kwargs):
        timestart = timestart if type(timestart) == datetime else validate_date(timestart)
        if not os.path.exists(input_filename):
            raise FileNotFoundError("File: %s not found" % input_filename)
        if is_text_file(input_filename):
            return super().load(cls,connection, input_filename, **kwargs)
        importRaster(input_filename, connection.db_params)
        result = upsertObservacionRaster(
            connection.db_params,
            date = timestart,
            series_id = series_id,
            return_values=True,
            **kwargs)
        if result is None:
            raise Exception("Creation failed")

        return [cls(**result)]
