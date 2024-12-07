from sqlalchemy import Column, Integer, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from .a5_base import A5Base
from .base import Base

class ObservacionAbstract(A5Base, Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestart = Column(TIMESTAMP(timezone=False), nullable=False)
    timeend = Column(TIMESTAMP(timezone=False), nullable=False)
    timeupdate = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.now())
    validada = Column(Boolean, default=False)
