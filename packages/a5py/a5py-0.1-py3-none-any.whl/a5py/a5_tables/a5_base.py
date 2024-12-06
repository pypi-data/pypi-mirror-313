from ..util import get_geometry_columns, model_to_dict

class A5Base:

    def get_geometry_columns(self):
        return get_geometry_columns(self)

    def to_dict(self, geometry_to_geojson = False, datetime_to_str = False):
        return model_to_dict(self, geometry_to_geojson = geometry_to_geojson, datetime_to_str = datetime_to_str)     
