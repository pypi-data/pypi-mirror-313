from ..util import get_geometry_columns, model_to_dict, readJson
import os

class A5Base:

    def get_geometry_columns(self):
        return get_geometry_columns(self)

    def to_dict(self, geometry_to_geojson = False, datetime_to_str = False):
        return model_to_dict(self, geometry_to_geojson = geometry_to_geojson, datetime_to_str = datetime_to_str)     

    @classmethod
    def load(cls, connection, input_filename : str, **kwargs):
        if not os.path.exists(input_filename):
            raise FileNotFoundError("File %s not found" % input_filename)
        created = connection.create(cls.__name__, input_filename, returning = True, **kwargs)
        if not len(created):
            raise Exception("Creation failed")
        return created
