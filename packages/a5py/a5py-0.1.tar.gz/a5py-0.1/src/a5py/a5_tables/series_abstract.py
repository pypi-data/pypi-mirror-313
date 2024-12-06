from sqlalchemy import Column, Integer, String
from .a5_base import A5Base
from .base import Base

class SerieAbstract(A5Base, Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)    
    var_id = Column(Integer)
    proc_id = Column(Integer)
    unit_id = Column(Integer)
    nombre = Column(String)
