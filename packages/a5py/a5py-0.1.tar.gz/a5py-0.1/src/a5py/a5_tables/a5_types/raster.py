from sqlalchemy.types import UserDefinedType
from sqlalchemy.sql import func

class Raster(UserDefinedType):
    cache_ok = True

    def get_col_spec(self):
        return "raster"
    
    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if isinstance(value, str):
                return value.encode()  # Convert string to bytes
            return value
        return process

    def default_query(self, column):
        # Use ST_AsGDALRaster with GeoTIFF format by default
        return func.ST_AsGDALRaster(column, 'GTiff')
