import subprocess
import unittest
import os
from rasterio import open as rio_open, DatasetReader
from rasterio.errors import RasterioIOError
from a5py.config import config

class TestCLIGeoTIFF(unittest.TestCase):
    def setUp(self):
        """Setup for tests: define paths and cleanup any previous outputs."""
        self.output_file = os.path.join(config.get("raster","path"),"output_test.tif")
        # Ensure no leftover files from previous runs
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def tearDown(self):
        """Cleanup after tests."""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_cli_produces_valid_geotiff(self):
        """Test if the CLI command produces a valid GeoTIFF."""
        # Replace with your actual CLI command
        command = ["python", "abm.py", "export", "2009-02-10" , self.output_file]
        
        # Run the CLI command
        subprocess.run(command, check=True)

        # Check if the file exists
        self.assertTrue(os.path.exists(self.output_file), "Output file was not created")

        # Validate the GeoTIFF using rasterio
        try:
            with rio_open(self.output_file) as dataset:
                # Check CRS and dimensions as an example validation
                self.assertIsNotNone(dataset.crs, "GeoTIFF has no CRS")
                self.assertGreater(dataset.width, 0, "GeoTIFF width is invalid")
                self.assertGreater(dataset.height, 0, "GeoTIFF height is invalid")
                self.assertIsInstance(dataset, DatasetReader, "The return value is not a DatasetReader")
                expected_width = (float(float(config.get("raster","bbox.lrx"))) - float(config.get("raster","bbox.ulx"))) * 240 + 1
                expected_height = (float(config.get("raster","bbox.uly")) - float(config.get("raster","bbox.lry"))) * 240 + 1
                self.assertEqual(dataset.width, expected_width, "Expected width == %d, got %d" % (expected_width, dataset.width))
                self.assertEqual(dataset.height, expected_height, "Expected height == %d, got %d" % (expected_height, dataset.height))
                self.assertAlmostEqual(dataset.bounds.left, float(config.get("raster","bbox.ulx")),2, "Expected bounds.left == %f, got %f" % (float(config.get("raster","bbox.ulx")), dataset.bounds.left))
                self.assertAlmostEqual(dataset.bounds.right, float(float(float(config.get("raster","bbox.lrx")))),2, "Expected bounds.right == %f, got %f" % (float(float(float(config.get("raster","bbox.lrx")))), dataset.bounds.right))
                self.assertAlmostEqual(dataset.bounds.top, float(config.get("raster","bbox.uly")), 2,"Expected bounds.top == %f, got %f" % (float(config.get("raster","bbox.uly")), dataset.bounds.top))
                self.assertAlmostEqual(dataset.bounds.bottom, float(config.get("raster","bbox.lry")), 2, "Expected bounds.bottom == %f, got %f" % (float(config.get("raster","bbox.lry")), dataset.bounds.bottom))
                
        except RasterioIOError:
            self.fail("Output file is not a valid GeoTIFF")

if __name__ == "__main__":
    unittest.main()
