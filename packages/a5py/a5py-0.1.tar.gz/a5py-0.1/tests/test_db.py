import unittest
from unittest.mock import patch
from a5py.config import config
from a5py.util import serialize_connection_string, validate_geojson
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from shapely.geometry import Polygon
from geoalchemy2.shape import from_shape, to_shape
from a5py.a5_tables.base import Base
import a5py.a5_tables as a5_tables
from a5py.util import readGeoJson
import tempfile
import json
from datetime import datetime, timedelta
from a5py.a5_connection import Connection
import logging
import subprocess
import os

test_db_params = {"protocol": "postgresql", **{option: config.get("test_db_params",option) for option in config.options("test_db_params")}}

test_db_connection_string = serialize_connection_string(test_db_params)

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the database, schema, and connection for testing.
        """
        cls.url = test_db_connection_string

        cls.engine = create_engine(cls.url)  
        
        # Create a session factory
        cls.Session = sessionmaker(bind=cls.engine)
        
        # Drop the schema (tables)
        Base.metadata.drop_all(cls.engine)
        
        # Create the schema (tables)
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        """
        Drop the database or close the connection.
        """
        Base.metadata.drop_all(cls.engine)  # Drops all tables
        cls.engine.dispose()  # Close the engine connection

    def setUp(self):
        """
        Create a new session before each test.
        """
        self.session = self.Session()
        for model in a5_tables.__all__:
            self.session.query(getattr(a5_tables,model)).delete()
        self.session.commit()


    def tearDown(self):
        """
        Rollback the session after each test.
        """
        self.session.rollback()
        for model in a5_tables.__all__:
            self.session.query(getattr(a5_tables,model)).delete()
        self.session.commit()
        self.session.close()

    def test_area_insert(self):

        # Insert data
        new_geom = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        new_area = a5_tables.Area(
            geom = from_shape(new_geom), 
            nombre = "Test area", 
            id = 1)
        self.session.add(new_area)
        self.session.commit()

        # Query data
        result = self.session.query(a5_tables.Area).filter_by(id=1).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.nombre, "Test area")
        self.assertTrue(new_geom.equals(to_shape(result.geom)))

        # delete data
        self.session.delete(new_area)
        self.session.commit()


    def test_serie_insert(self):

        # Insert data
        new_geom = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        new_area = a5_tables.Area(
            geom = from_shape(new_geom), 
            nombre = "Test area", 
            id = 1)
        self.session.add(new_area)
        new_serie = a5_tables.SerieAreal(area_id=new_area.id, id=1, var_id= 30, proc_id = 5, unit_id = 14, fuentes_id = 40)
        self.session.add(new_serie)
        self.session.commit()

        # Query data
        result = self.session.query(a5_tables.SerieAreal).filter_by(area_id=1, fuentes_id=40).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.proc_id, 5)
        self.assertEqual(result.unit_id, 14)
        self.assertTrue(new_geom.equals(to_shape(result.area.geom)))

        # delete data
        self.session.delete(new_area)
        self.session.delete(new_serie)
        self.session.commit()

    def test_import_geojson(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/sample_geom.json"
            data = sample_area_geojson
            with open(file_path, 'w') as f:
                json.dump(data, f)
            
            # read geojson
            new_area = readGeoJson(a5_tables.Area, file_path)[0]

            # insert
            self.session.add(new_area)
            self.session.commit()

            # Query data
            result = self.session.query(a5_tables.Area).filter_by(id=1).first()
            self.assertIsNotNone(result)
            self.assertEqual(result.nombre, "Test area")
            self.assertTrue(to_shape(new_area.geom).equals(to_shape(result.geom)))

            # delete data
            self.session.delete(new_area)
            self.session.commit()

    def test_rast_2_areal(self):

        rast_series_id = 19
        area_id = 1
        timestart = datetime(2000,1,1)
        timeend = datetime(2000,1,4)
        rast_valor = 33

        # create serie
        self.session.add(
            a5_tables.SerieRast(
                id = 19,
                fuentes_id = 40
            )
        )

        # create rast obs
        t = timestart
        while t < timeend:
            logging.debug("create rast: %s" % t.isoformat())
            self.session.add(
                a5_tables.ObservacionRast(
                    series_id = rast_series_id,
                    timestart = t,
                    timeend = t + timedelta(days=1),
                    valor = func.st_asraster(
                        func.st_geomfromtext('LINESTRING(0 0, 1 0, 1 1, 0 1, 0 0)', 4326), 
                        200, 
                        200,
                        ['8BUI'],
                        [rast_valor],
                        [2]
                    )
                )
            )
            t = t + timedelta(days=1)
        
        # create area
        self.session.add(a5_tables.Area(
            id = area_id,
            nombre="Test area",
            geom=from_shape(Polygon([(0, 0), (0.5, 0), (0.5, 1), (0, 1), (0, 0)]))
        ))

        self.session.commit()
        # self.session.close()

        # get areal means for area
        connection = Connection(self.url)

        areal_means = connection.query_rast_2_areal(
            area_id, 
            rast_series_id, 
            timestart, 
            timeend, 
            agg_func = "mean",
            areal_series_id = None,
            insert = False,
            on_conflict = "update"
        )

        for obs in areal_means:
            self.assertEqual(type(obs.valor), float, "Expected a float, got %s" % type(obs.valor))
            self.assertAlmostEqual(obs.valor, rast_valor, 2, "Mean = %f expected, got %f" % (rast_valor, obs.valor))

        # get count
        areal_counts = connection.query_rast_2_areal(
            area_id, 
            rast_series_id, 
            timestart, 
            timeend, 
            agg_func = "count",
            areal_series_id = None,
            insert = False,
            on_conflict = "update"
        )

        for obs in areal_counts:
            self.assertEqual(type(obs.valor), float, "Expected a float, got %s" % type(obs.valor))
            self.assertAlmostEqual(obs.valor, 299, 2, "count = %f expected, got %f" % (299, obs.valor))
        
        connection.session.close()

        # CLI
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/serie_areal.json"
            command = [
                "a5py", 
                "rast2areal", 
                str(rast_series_id), 
                str(area_id), 
                timestart.isoformat(), 
                timeend.isoformat(), 
                "-a",
                "count",
                "-c",
                "update",
                "-u",
                self.url,
                "-o",
                file_path]
            result = subprocess.run(command, check=True)
            self.assertEqual(result.returncode, 0, "Got return code %d from subprocess" % result.returncode)
            self.assertTrue(os.path.exists(file_path),"File %s not found" % file_path)
            
            with open(file_path,"r") as file:
                try:
                    areal_counts = json.load(file)
                except json.JSONDecodeError as e:
                    self.fail(f"{e}")
                self.assertEqual(type(areal_counts), list, "Expected a list")
                self.assertEqual(len(areal_counts), 3, "Expected 3 areal obs")
                for obs in areal_counts:
                    self.assertEqual(type(obs["valor"]), float, "Expected a float, got %s" % type(obs["valor"]))
                    self.assertAlmostEqual(obs["valor"], 299, 2, "count = %f expected, got %f" % (299, obs["valor"]))
        
        # insert areal
        new_serie = a5_tables.SerieAreal(area_id=1, id=1, var_id= 30, proc_id = 5, unit_id = 14, fuentes_id = 40)
        self.session.add(new_serie)
        self.session.commit()

        command = [
                "a5py", 
                "rast2areal", 
                str(rast_series_id), 
                str(area_id), 
                timestart.isoformat(), 
                timeend.isoformat(), 
                "-a",
                "count",
                "-c",
                "update",
                "-u",
                self.url,
                "-i",
                "-s",
                "1"]
        result = subprocess.run(command, check=True)
        self.assertEqual(result.returncode, 0, "Got return code %d from subprocess" % result.returncode)
        connection.reopen()
        obs_areal = connection.read("ObservacionAreal",series_id=1)
        self.assertEqual(len(obs_areal),3,"Expected 3 obs areal")
        for obs in obs_areal:
            self.assertAlmostEqual(obs_areal[0].valor,299,"Expected valor=299")

    def test_create_area(self):
        connection = Connection(self.url)
        try:
            for json_object in [(sample_area_geojson, True), (sample_area_json, False), (sample_area_geojson_con_exutorio, True)]:

                with tempfile.TemporaryDirectory() as temp_dir:
                    file_path = f"{temp_dir}/sample_area.json"
                    data = json_object[0]
                    with open(file_path, 'w') as f:
                        json.dump(data, f)
                    
                    for input_json in [file_path, json.load(open(file_path))]:
                        
                        new_areas = connection.create("Area", input_json, geojson = json_object[1], returning=True)

                        self.assertEqual(len(new_areas), 1, "Expected %d created Area, got %d" % (1, len(new_areas)))
                        self.assertEqual(new_areas[0].id, 1, "Expected id=%d, got %d" % (1, new_areas[0].id))

                        # Query data
                        result = self.session.query(a5_tables.Area).filter_by(id=1).first()
                        self.assertIsNotNone(result)
                        self.assertEqual(result.nombre, "Test area")
                        self.assertTrue(to_shape(new_areas[0].geom).equals(to_shape(result.geom)))

                        no_results = connection.create("Area", file_path, geojson = json_object[1], returning=True, on_conflict="nothing")

                        self.assertEqual(len(no_results), 0, "Expected 0 created Area, got %d" % (len(no_results)))

                        # Query data
                        results = self.session.query(a5_tables.Area).all()
                        self.assertIsNotNone(results)
                        self.assertEqual(len(results),1, "expected 1 area from query, got %s" % len(results))

                        # delete
                        self.session.delete(results[0])
                        self.session.commit()
        except Exception as e:
            raise
        finally:
            connection.cleanup()

    def test_create_area_on_conflict(self):
        connection = Connection(self.url)
        try:
            for json_object in [(sample_area_geojson, True), (sample_area_json, False)]:

                with tempfile.TemporaryDirectory() as temp_dir:
                    file_path = f"{temp_dir}/sample_area.json"
                    data = json_object[0]
                    with open(file_path, 'w') as f:
                        json.dump(data, f)
                    
                    for input_json in [file_path, json.load(open(file_path))]:
                        areas_1 = connection.create("Area", input_json, geojson = json_object[1], returning=True)
                        
                        no_upserted = connection.create("Area", input_json, geojson = json_object[1], on_conflict = "nothing", returning=True)

                        self.assertEqual(len(no_upserted), 0, "no upserts expected, got %d" % len(no_upserted))

                        upserted = connection.create("Area", input_json, geojson = json_object[1], on_conflict = "update", returning=True)

                        self.assertEqual(len(upserted), 1, "1 upserts expected, got %d" % len(upserted))

                        with self.assertRaises(IntegrityError):
                            connection.create("Area", input_json, geojson = json_object[1], on_conflict = None, returning=True)
                            # "Expected raise error because of conflicting rows"
                        
                        connection.session.rollback()
                        connection.session.query(a5_tables.Area).delete()

        except Exception as e:
            raise
        finally:
            connection.cleanup()

    def test_create_area_cli(self):
        for json_object in [(sample_area_geojson, True, True), (sample_area_json, False, True), (sample_area_json_array, False, True),(sample_area_json_dict, False, False)]:

            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = f"{temp_dir}/sample_area.json"
                data = json_object[0]
                with open(file_path, 'w') as f:
                    json.dump(data, f)
                
                for input_json in [file_path, json.dumps(json.load(open(file_path)))]:

                    command = ["a5py", "create", "-u",self.url,input_json]            
                    if json_object[1]:
                        command.append("-g")
                    if json_object[2]:
                        command.extend(["-m", "Area"])
                    result = subprocess.run(command, check=True)
                    self.assertEqual(result.returncode, 0, "Process failed with return code %d" % result.returncode)

                    # Query data
                    results = self.session.query(a5_tables.Area).all()
                    self.assertIsNotNone(results)
                    self.assertEqual(len(results),1, "expected 1 area from query, got %s" % len(results))

                    # delete
                    self.session.delete(results[0])
                    self.session.commit()
    
    def test_read_area(self):
        connection = Connection(self.url)
        try:
            connection.create("Area",sample_area_json)
            result = connection.read("Area",id=1)

            self.assertEqual(len(result),1, "Expected 1 result")
            self.assertTrue(hasattr(result[0],"id"), "Expected id attr in result")
            self.assertEqual(result[0].id, 1, "Expected id=1")
            self.assertTrue(hasattr(result[0],"geom"), "Expected geom attr in result")
            self.assertEqual(str(type(result[0].geom)), "<class 'geoalchemy2.elements.WKBElement'>", "Expected geom attr of type <class 'geoalchemy2.elements.WKBElement'>. Got %s" % type(result[0].geom))
            # self.assertEqual(sample_area_json.geom, result[0]["geom"], "Different geom")
        except Exception as e:
            self.fail(f"{e}")
        finally:
            connection.cleanup()

    def test_read_area_geojson(self):
        connection = Connection(self.url)
        try:
            connection.create("Area",{**sample_area_json})
            result = connection.read("Area",geojson=True, id=1)

            self.assertEqual(type(result),dict, "Expected dict result")
            self.assertTrue("features" in result, "Expected features attr in result")
            self.assertEqual(len(result["features"]), 1, "expected features length 1")
            self.assertTrue("properties" in result["features"][0], "Expected properties property")
            self.assertEqual(result["features"][0]["properties"]["id"], 1, "Expected id=1")
            self.assertTrue("geometry" in result["features"][0], "Expected geometry property")
            self.assertEqual(type(result["features"][0]["geometry"]), dict, "Expected geometry of dict type. Got %s" % type(result["features"][0]["geometry"]))
            self.assertEqual(json.dumps(sample_area_json["geom"]), json.dumps(result["features"][0]["geometry"]), "Different geom")
        except Exception as e:
            raise
        finally:
            connection.cleanup()

    def test_read_area_bad_id(self):
        connection = Connection(self.url)
        try:
            connection.create("Area",sample_area_json)
            result = connection.read("Area",id=2)

            self.assertEqual(len(result),0, "Expected 0 result")
        except Exception as e:
            raise
        finally:
            connection.cleanup()

    def test_read_area_cli(self):
        # read all areas in json format

        connection = Connection(self.url)
        try:
            connection.create("Area",[*sample_area_json_array])
        finally:
            connection.cleanup()

        for fmt in ["json", "geojson"]:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = f"{temp_dir}/areas.%s" % fmt
                command = ["a5py", "read", "Area", file_path, "-u", self.url] 
                if fmt == "geojson":
                    command.append("-g")
                result = subprocess.run(command, check=True)
                self.assertEqual(result.returncode, 0, "Process failed with return code %d" % result.returncode)
                self.assertTrue(os.path.exists(file_path), "Output file not found")
                
                # read file
                with open(file_path, "r") as f:
                    content = f.read()
                try:
                    parsed_content = json.loads(content)
                except json.JSONDecodeError:
                    self.fail("The file content is not valid JSON.")

                if fmt == "geojson":
                    self.assertTrue(validate_geojson(parsed_content), "Not a valid geojson")
                    self.assertEqual(len(parsed_content["features"]), len(sample_area_json_array), "Expected length %d" % len(sample_area_json_array))
                    for index, item in enumerate(parsed_content["features"]):
                        self.assertEqual(type(item), dict, "Expected a dict")
                        self.assertTrue("properties" in item, "Expected properties property")
                        self.assertEqual(type(item["properties"]), dict, "Expected a properties dict")
                        for k, v in item["properties"].items():
                            if k in sample_area_json_array[index]:
                                self.assertEqual(v, sample_area_json_array[index][k], "output file differs from original object at index %d, key %s" % (index, k))
                        self.assertEqual(item["geometry"], sample_area_json_array[index]["geom"], "Geometry differs")
                else:
                    self.assertEqual(type(parsed_content), list, "Expected a list")
                    self.assertEqual(len(parsed_content), len(sample_area_json_array),"Expected length: %d" % len(sample_area_json_array))
                    for index, item in enumerate(parsed_content):
                        self.assertEqual(type(item), dict, "Expected a dict")
                        for k, v in item.items():
                            if k in sample_area_json_array[index]:
                                self.assertEqual(v, sample_area_json_array[index][k], "output file differs from original object at index %d, key %s" % (index, k))

    def test_read_area_filter_no_results(self):
        
        connection = Connection(self.url)
        try:
            connection.create("Area",[*sample_area_json_array])
        finally:
            connection.cleanup()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/areas.json"
            command = ["a5py", "read", "Area", file_path, "-u", self.url, "-f", "id=2"]
            result = subprocess.run(command, check=True)
            self.assertEqual(result.returncode, 0, "Process failed with return code %d" % result.returncode) 
            self.assertTrue(os.path.exists(file_path), "Output file not found")
                
            # read file
            with open(file_path, "r") as f:
                content = f.read()
            try:
                parsed_content = json.loads(content)
            except json.JSONDecodeError:
                self.fail("The file content is not valid JSON.")
            
            # expect an empty list
            self.assertEqual(type(parsed_content), list, "Expected a list")
            self.assertEqual(len(parsed_content), 0, "Expected 0 length")

    def test_read_area_filter_1_result(self):
        
        sample2 = {**sample_area_json}
        sample2["id"] = 2
        sample2["nombre"] = "Area 2"

        connection = Connection(self.url)
        try:
            connection.create("Area",[*sample_area_json_array, sample2])
        finally:
            connection.cleanup()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/areas.json"

            for index, flt in enumerate(["id=2", "nombre=Area 2", None]):
                command = ["a5py", "read", "Area", file_path, "-u", self.url]
                if flt is not None:
                    command.extend([ "-f", flt])
                result = subprocess.run(command, check=True)
                self.assertEqual(result.returncode, 0, "Process failed with return code %d" % result.returncode) 
                self.assertTrue(os.path.exists(file_path), "Output file not found")
                    
                # read file
                with open(file_path, "r") as f:
                    content = f.read()
                try:
                    parsed_content = json.loads(content)
                except json.JSONDecodeError:
                    self.fail("The file content is not valid JSON.")
                
                # expect 1 element in list
                self.assertEqual(type(parsed_content), list, "Expected a list")
                if flt is not None:
                    self.assertEqual(len(parsed_content), 1, "Expected 1 length")
                    self.assertEqual(parsed_content[0]["id"], 2, "Expected id=2")
                    self.assertEqual(parsed_content[0]["nombre"], "Area 2", "Expected nombre=Area 2")
                else:
                    self.assertEqual(len(parsed_content), 2, "Expected 2 length")

    def test_read_area_bad_filter_key(self):
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/areas.json"
            command = ["a5py", "read", "Area", file_path, "-u", self.url, "-f", "badfilterkey=2"]

            with self.assertRaises(subprocess.CalledProcessError):
                result = subprocess.run(command, check=True)

    def test_update_area(self):
        connection = Connection(self.url)
        try:
            connection.create("Area",sample_area_json)
            connection.update("Area", nombre="Nombre nuevo")
            result = connection.read("Area",id=1)
    
            self.assertEqual(len(result),1, "1 item expected")
            self.assertEqual(result[0].nombre,"Nombre nuevo", "field nombre not correctly updated. Got: %s" % result[0].nombre)

            # update geom
            new_geom = {"type": "Polygon", "coordinates": [[[-53.0,-34.0],[-51.0,-34.0],[-51.0,-32.0],[-53.0,-32.0],[-53.0,-34.0]]]}
            connection.update("Area", geom=new_geom)
            result = connection.read("Area",id=1)
            self.assertEqual(type(result), list, "Expected a list")
            self.assertEqual(len(result),1, "1 item expected")
            result_dict = result[0].to_dict(True)
            self.assertEqual(json.dumps(result_dict["geom"]),json.dumps(new_geom), "field geom not correctly updated. Got: %s" % str(result_dict["geom"]))
        except Exception as e:
            self.fail(f"{e}")
        finally:
            connection.cleanup()

    def test_update_area_cli(self):
        connection = Connection(self.url)
        try:
            connection.create("Area",sample_area_json)
        except Exception as e:
            self.fail(f"{e}")
        finally:
            connection.cleanup()
        
        for index, flt in enumerate(["id=2","id=1"]):
            command = ["a5py", "update", "Area", "nombre=Nuevo nombre", "-u", self.url]
            if flt is not None:
                command.extend([ "-f", flt])
            result = subprocess.run(command, check=True)
            self.assertEqual(result.returncode, 0, "Process failed with return code %d" % result.returncode)

            #read updated
            try:
                connection.reopen()
                updated = connection.read("Area",filters={"id":1})
                if index == 0:
                    self.assertEqual(updated[0].nombre, "Test area")
                else:
                    self.assertEqual(updated[0].nombre, "Nuevo nombre")

            except Exception as e:
                self.fail(f"{e}")
            finally:
                connection.cleanup()
        
    @patch('builtins.input', return_value='yes')
    def test_delete_area(self, mock_input):
        connection = Connection(self.url)
        try:
            sample2 = {**sample_area_json}
            sample2["id"] = 2
            sample2["nombre"] = "Area 2"
            connection.create("Area",[*sample_area_json_array, sample2])
            deleted = connection.delete("Area", id=1)
            mock_input.assert_called_once_with("Do you want to proceed with deletion of 1 records? (yes/no): ")
            self.assertEqual(len(deleted),1, "Expected 1 deleted object")
            self.assertEqual(deleted[0].id,1, "Expected id = 1")
            result = connection.read("Area")  
            self.assertEqual(len(result),1, "1 item expected")
            self.assertEqual(result[0].id,2, "Expected id = 2")
            result = connection.read("Area",id=1)  
            self.assertEqual(len(result),0, "0 item expected")

        except Exception as e:
            self.fail(f"{e}")
        finally:
            connection.cleanup()

    def test_delete_area_cli(self):
        connection = Connection(self.url)
        try:
            sample2 = {**sample_area_json}
            sample2["id"] = 2
            sample2["nombre"] = "Area 2"
            connection.create("Area",[*sample_area_json_array, sample2])
        except Exception as e:
            self.fail(f"{e}")
        finally:
            connection.cleanup()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/sample_geom.json"
            command = ["a5py", "delete", "Area", "-f", "id=1","-u",self.url,"-o",file_path,"-s"]  
            result = subprocess.run(command, check=True)
            self.assertEqual(result.returncode, 0, "Process failed with return code %d" % result.returncode)
            self.assertTrue(os.path.exists(file_path))
            try:
                connection.reopen()
                result = connection.read("Area")  
                self.assertEqual(len(result),1, "1 item expected")
                result = connection.read("Area",id=1)  
                self.assertEqual(len(result),0, "0 item expected")
            except Exception as e:
                self.fail(f"{e}")
            finally:
                connection.cleanup()



sample_geometry = {
    "type": "Polygon",
    "coordinates": [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]
}

sample_area_geojson = {
    "type": "FeatureCollection", 
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": 1,
                "nombre": "Test area"
            },
            "geometry": sample_geometry
        }
    ]
}

sample_area_json = {
    "id": 1,
    "nombre": "Test area",
    "geom": sample_geometry
}

sample_area_json_array = [ sample_area_json ]

sample_area_json_dict = {
    "Area": sample_area_json_array
}

sample_area_geojson_con_exutorio = {
    "type": "FeatureCollection", 
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": 1,
                "nombre": "Test area",
                "exutorio": {
                    "type": "Point",
                    "coordinates": [0, 0]
                }
            },
            "geometry": sample_geometry
        }
    ]
}
        

            



if __name__ == '__main__':
    unittest.main()



