from a5py.config import config
from a5py.util import serialize_connection_string
from a5py.a5_connection import Connection
from a5py import ObservacionRast 
import unittest
import rasterio
from io import BytesIO

connection_dict = {"protocol":"postgresql",**{option: config.get("db_params",option) for option in config.options("db_params")}}

connection_string = serialize_connection_string(connection_dict)

class TestValorIsBytes(unittest.TestCase):

    def test_valor_is_bytes(self):
        url = connection_string
        connection = Connection(url)
        observaciones = connection.query_with_filter(ObservacionRast, {"timestart": "2009-02-10"})
        self.assertEqual(type(observaciones[0].valor), bytes)

    def test_query_as_gdal(self):
        url = connection_string
        connection = Connection(url)
        observaciones = connection.query_observaciones_rast({"timestart": "2009-02-10"})
        self.assertEqual(type(observaciones[0].valor), memoryview, "the return value is not a memoryview")
        # Convert bytes to a file-like object
        geotiff_file = BytesIO(observaciones[0].valor)

        # Open the dataset using rasterio
        with rasterio.open(geotiff_file) as dataset:
            self.assertIsInstance(dataset, rasterio.DatasetReader, "The return value is not a DatasetReader")
            expected_width = (float(config.get("raster","bbox.lrx")) - float(config.get("raster","bbox.ulx"))) * 240 + 1
            expected_height = (float(config.get("raster","bbox.uly")) - float(config.get("raster","bbox.lry"))) * 240 + 1
            self.assertEqual(dataset.width, expected_width, "Expected width == %d, got %d" % (expected_width, dataset.width))
            self.assertEqual(dataset.height, expected_height, "Expected height == %d, got %d" % (expected_height, dataset.height))
            self.assertAlmostEqual(dataset.bounds.left, float(config.get("raster","bbox.ulx")),2, "Expected bounds.left == %f, got %f" % (float(config.get("raster","bbox.ulx")), dataset.bounds.left))
            self.assertAlmostEqual(dataset.bounds.right, float(config.get("raster","bbox.lrx")),2, "Expected bounds.right == %f, got %f" % (float(config.get("raster","bbox.lrx")), dataset.bounds.right))
            self.assertAlmostEqual(dataset.bounds.top, float(config.get("raster","bbox.uly")), 2,"Expected bounds.top == %f, got %f" % (float(config.get("raster","bbox.uly")), dataset.bounds.top))
            self.assertAlmostEqual(dataset.bounds.bottom, float(config.get("raster","bbox.lry")), 2, "Expected bounds.bottom == %f, got %f" % (float(config.get("raster","bbox.lry")), dataset.bounds.bottom))
        