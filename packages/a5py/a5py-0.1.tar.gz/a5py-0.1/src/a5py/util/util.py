import psycopg2
import copy
from psycopg2.extras import RealDictCursor
from typing import List
import subprocess
from datetime import datetime
import glob
import re
import os
import argparse
from shapely.geometry import shape
from shapely import from_wkt # wkb
import json
from typing import Union, Dict, Any
from geoalchemy2 import Geometry, WKBElement
# from geoalchemy2.functions import ST_AsGeoJSON
from geoalchemy2.shape import to_shape
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.exc import IntegrityError
# from sqlalchemy import inspect
import logging

GeoJSON = Dict[str, Any]

def get_geometry_columns(model):
    return {
        column_name: column
        for column_name, column in model.__mapper__.columns.items()
        if isinstance(column.type, Geometry)
    }

def instantiate_model(Model : type, properties : dict, geometry_column : str = None, geometry : dict = None):
    """Instantiate a5 orm model from dict

    Args:
        Model (type): a5 orm model
        properties (dict): key-value pairs to populate the columns
        geometry_column (str, optional): name of the geometry column. If None, geometry columns are detected where to the column type is Geometry. Defaults to None.
        geometry (dict, optional): geojson-type geometry to assign to the geometry column. If None and geometry_column is not None, reads geometry from propeties[geometry_column]. Defaults to None.

    Raises:
        ValueError: If geometry is None, geometry_column is not None, and geometry_column is not in properties

    Returns:
        Model: Instance of Model class
    """
    geometry_columns = get_geometry_columns(Model)
    if len(geometry_columns):
        for column_name in geometry_columns.keys():
            if column_name in properties:
                properties[column_name] = shape(properties[column_name]).wkt if type(properties[column_name]) == dict else properties[column_name]
    if geometry_column is not None:
        if geometry is not None:
            properties[geometry_column] =  shape(geometry).wkt
        elif geometry_column not in properties:
            raise ValueError("Geometry column %s missing in properties" % geometry_column)
        else:
            properties[geometry_column] = shape(properties[geometry_column]).wkt
    return Model(**properties)

def readGeoJson(Model : type, geojson : Union[str,dict], geometry_column : str = "geom") -> list:
    """Read and convert geojson features into orm model objects"""
    if type(geojson) == str:
        with open(geojson,"r") as f:
            geojson_data = json.load(f)
    else:
        geojson_data = {**geojson} 
    result = []
    for feature in geojson_data["features"]:
        result.append(instantiate_model(Model, feature["properties"], geometry_column, feature["geometry"]))
    return result

def readJson(Model : type, data : Union[str,dict,list], geometry_column : str = None) -> list:
    """Read and convert json objects into orm model objects"""
    if type(data) == str:
        with open(data,"r") as f:
            json_data = json.load(f)
    else:
        json_data = copy.deepcopy(data) 
    if type(json_data) == dict:
        return [ instantiate_model(Model, json_data, geometry_column) ]
    elif type(json_data) == list:
        result = []
        for item in json_data:
            result.append(instantiate_model(Model, item, geometry_column))
        # BaseGeometry
        return result
    else:
        raise TypeError("data must be of type str, dict or list")


class DBParams(dict):
    dbname : str
    username : str
    password : str
    host : str
    port : int

class ObservacionRaster(dict):
    id : int
    series_id : int
    timestart : datetime
    timeend : datetime
    valor : bytes
    timeupdate : datetime


# Function to sanitize table name
def sanitize_sql_identifier(table_name):
    if re.match(r'^[a-zA-Z0-9_]+$', table_name):
        return table_name
    else:
        raise ValueError("Invalid table name")

def query_psql_to_dict(
        query, 
        dbname : str, 
        username : str, 
        password : str  = None, 
        host : str = "localhost",
        port : int = 5432,
        query_params : list = []) -> List[dict]:
    """
    Executes a SQL query on a PostgreSQL database and returns the result as a list of dictionaries.
    """
    try:
        # Connect to the PostgreSQL database
        kwargs = {
            "dbname": dbname,
            "user": username,
            "password": password,
            "host": host,
            "port": port
        }
        if password is not None:
            kwargs["password"] = password
        
        conn = psycopg2.connect(
            **kwargs
        )
        
        result = []
        # Create a cursor that returns rows as dictionaries
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Execute the query
            # print(f"ejecuta query: {query}")
            cursor.execute(query, query_params)
            
            # Fetch all rows as a list of dictionaries
            rows = cursor.fetchall()
            print(f"resultados: {len(rows)}")
            # if len(rows):
            #     print(rows[0])
            conn.commit()
            result = rows
            cursor.close()
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        result = []
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()
    return result

def importRaster(
    filename : str,
    db_params : DBParams,
    tablename : str = "public.rastest",
):
    
    drop_table_command = [
        "psql",
        "-U",
        db_params["username"],
        "-d",
        db_params["dbname"],
        "-h",
        db_params["host"],
        "-p",
        str(db_params["port"]),
        "-c",
        "DROP TABLE IF EXISTS %s;" % tablename
    ]

    comando_raster2pgsql = [
        "raster2pgsql",
        "-F", "-d",
        filename,
        tablename
    ]
    psql_command = [
        "psql",
        "-U",
        db_params["username"],
        "-d",
        db_params["dbname"],
        "-h",
        db_params["host"],
        "-p",
        str(db_params["port"])
    ]

    env = None
    if db_params["password"] is not None:
        env = {
            "PGPASSWORD": db_params["password"]
        }

    # Ejecutar el comando raster2pgsql
    subprocess.run(drop_table_command, env = env)
    raster_process = subprocess.Popen(comando_raster2pgsql,  stdout=subprocess.PIPE, env = env)
    psql_process = subprocess.run(psql_command, stdin=raster_process.stdout, text=True, env = env)
    raster_process.stdout.close()
    if psql_process.returncode == 0:
        print("GeoTIFF imported successfully.")
    else:
        raise Exception(f"Error during import: {psql_process.stderr}, {raster_process.stderr}")

def upsertObservacionRaster(
    db_params : DBParams,
    date : datetime,
    series_id : int,
    reclassexpr : str = '[0]:0,[1]:1,2:[2]',
    data_type : str = "2BUI",
    srid : int = 4326,
    tablename : str = "rastest",
    columnname : str = "rast",
    return_values : bool = False
    ) -> ObservacionRaster:

    sanitize_sql_identifier(tablename)
    sanitize_sql_identifier(columnname)

    returning_columns = "id, series_id, timestart, timeend, valor, timeupdate" if return_values else "id, series_id, timestart, timeend, timeupdate"

    comando_insert = f"""
        INSERT INTO observaciones_rast (series_id, timestart, timeend, valor) 
            SELECT 
                %s, 
                %s, 
                %s, 
                ST_SetSRID(
                    ST_SetBandNoDataValue(
                        ST_Reclass(
                            "{columnname}",
                            %s,
                            %s
                        ),
                    2),
                %s) 
            FROM "{tablename}" 
        ON CONFLICT (series_id, timestart, timeend) 
            DO UPDATE SET 
                valor=excluded.valor, 
                timeupdate=excluded.timeupdate
        RETURNING {returning_columns};
    """

    # print(f"query string: {comando_insert}")

    result = query_psql_to_dict(
        comando_insert, 
        db_params["dbname"], 
        db_params["username"], 
        db_params["password"], 
        db_params["host"], 
        db_params["port"], 
        query_params = (series_id, date, date, reclassexpr, data_type, srid)
    )

    if len(result):
        return result[0]
    raise Exception("Error al intentar insertar observación")


def zipFiles(directory : str, pattern : str, decompress : bool = False):
    # Define the directory and regular expression
    pattern = re.compile(pattern)
    # Walk through the directory
    result = []
    for root, _, files in os.walk(directory):
        for file in files:
            if pattern.match(file):
                full_path = os.path.join(root, file)
                try:
                    # Use subprocess to call gzip
                    if decompress:
                        subprocess.run(['gzip','-d', full_path], check=True)
                        print(f"Decompressed: {full_path}")
                    else:
                        subprocess.run(['gzip', full_path], check=True)
                        print(f"Compressed: {full_path}")
                    result.append(full_path)
                except subprocess.CalledProcessError as e:
                    print(f"Error (de)compressing {full_path}: {e}")
    return result

def remove_files_in_dir(directory, pattern):
    # Create the full path pattern
    pattern_path = os.path.join(directory, pattern)
    
    # Get all files matching the pattern
    files_to_delete = glob.glob(pattern_path)
    
    # Remove each file
    for file in files_to_delete:
        try:
            os.remove(file)
            print(f"Removed: {file}")
        except Exception as e:
            print(f"Failed to remove {file}: {e}")

def validate_date(date_str):
    """Validate and parse a date string."""
    formats = [
        "%Y-%m-%d",             # Date only
        "%Y-%m-%d %H:%M",       # Date and time without seconds
        "%Y-%m-%d %H:%M:%S",    # Date and time with seconds
        "%Y-%m-%d %H:%M:%S%z",  # Date, time, and timezone
        "%Y-%m-%dT%H:%M:%S",    # ISO 8601 without timezone (asumes UTC)
        "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 with timezone
        "%Y-%m-%d %H:%M:%S.%f%z",  # Date, time, and timezone
        "%Y-%m-%dT%H:%M:%S.%f%z",  # ISO 8601 with timezone
        "%m-%d-%Y"              # date only, US format
    ]
    for format in formats:
        try:
            return datetime.strptime(date_str, format)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: '{date_str}'. Expected formats: YYYY-MM-DD, YYYY-MM-DD HH:MM, YYYY-MM-DD HH:MM:SS, YYYY-MM-DD HH:MM:SSZZZ, YYYY-MM-DDTHH:MM:SS, YYYY-MM-DDTHH:MM:SSZZZ, YYYY-MM-DD HH:MM:SS.mmmZZZ, YYYY-MM-DDTHH:MM:SS.mmmZZZ.")

def serialize_connection_string(params):
    """
    Convert the dictionary of connection parameters into a connection string.
    Example format: postgresql://user:password@localhost:5432/mydatabase
    """
    # Ensure all necessary parameters are in the dictionary
    required_keys = ['protocol', 'username', 'password', 'host', 'port', 'dbname']
    aliases = {
        'username': ["user"],
        'dbname': ["database"]
    }
    for key in required_keys:
        if key not in params:
            if key not in aliases:
                raise ValueError(f"Missing required parameter of database connection: {key}")
            for alias in aliases[key]:
                if alias in params:
                    params[key] = params[alias]
                    break
            else:
                raise ValueError(f"Missing required parameter of database connection: {key}")

    
    # Build the connection string
    connection_string = (f"{params['protocol']}://"
                         f"{params['username']}:{params['password']}@"
                         f"{params['host']}:{params['port']}/"
                         f"{params['dbname']}")
    return connection_string

def process_coordinates(values):
    """Convert a flat list of 4 floats into a 2-tuple of 2-tuples."""
    if len(values) != 4:
        raise argparse.ArgumentTypeError("Exactly 4 float values are required.")
    return ((values[0], values[1]), (values[2], values[3]))

def valid_date(date_str):
    try:
        return validate_date(date_str)
    except ValueError as e:
        raise argparse.ArgumentTypeError(e)

def parse_connection_string(connection_string):
    """
    Parse the connection string and return its components as a dictionary.
    Example format: postgresql://user:password@localhost:5432/mydatabase
    """
    # Regular expression to match a typical connection string format
    pattern = re.compile(r'^(?P<protocol>\w+)://(?P<username>\w+):(?P<password>\w+)@(?P<host>[\w.]+):(?P<port>\d+)/(?P<dbname>\w+)$')
    match = pattern.match(connection_string)
    
    if not match:
        raise ValueError(f"Invalid connection string format: {connection_string}")
    
    # Extract components using named groups
    connection_params = match.groupdict()
    connection_params['port'] = int(connection_params['port'])  # Ensure the port is an integer
    return connection_params

def insert(
        session, 
        model : type,
        values : Union[dict,list],
        on_conflict_do_nothing : bool = False, 
        returning : bool = False) -> Union[None, list]:
    stmt = pg_insert(model).values(values)
    if on_conflict_do_nothing:
        stmt = stmt.on_conflict_do_nothing()
    primary_key = get_primary_keys(model)[0]
    stmt = stmt.returning(primary_key)
    try:
        inserted_ids = session.execute(stmt)
    except IntegrityError as e:
        # logging.error(str(e))
        raise
    session.commit()
    inserted_ids = [r[0] for r in inserted_ids]
    if not on_conflict_do_nothing:
        if type(values) == dict and len(inserted_ids) == 0:
            raise Exception("No rows inserted")
        elif len(inserted_ids) != len(values):
            raise Exception("Expected insertions: %d, inserted %d rows" % (len(values), inserted_ids))
    if returning:
        results = session.query(model).filter(primary_key.in_(inserted_ids)).all()
        return results
    return 


def upsert(session, model, values, returning : bool = False):
    """
    Perform an upsert (insert or update) based on the model definition.
    
    :param session: SQLAlchemy session
    :param model: SQLAlchemy model class
    :param values: Dictionary of values to insert/update
    :param returning: if True, return insert/update result
    """
    # Extract unique constraints or primary key columns as index_elements
    table = model.__table__
    index_elements = [col.name for col in table.columns if col.primary_key or col.unique]

    if not index_elements:
        stmt = pg_insert(model).values(values)
        # raise ValueError("No unique or primary key constraint found for upsert operation.")

    else:
        # Generate excluded values dynamically
        excluded_values = {col.name: getattr(pg_insert(model).excluded, col.name) for col in table.columns if col.name not in index_elements}

        # Create the insert statement with ON CONFLICT DO UPDATE
        stmt = pg_insert(model).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=index_elements,
            set_=excluded_values
        )

    # Execute the statement
    primary_key = get_primary_keys(model)[0]
    stmt = stmt.returning(primary_key)
    upserted_ids =  session.execute(stmt)
    session.commit()
    upserted_ids = [r[0] for r in upserted_ids]
    if returning:
        results = session.query(model).filter(primary_key.in_(upserted_ids)).all()
        return results
    return



def get_primary_keys(model):

    # Get the class mapper for the model
    mapper = class_mapper(model)

    # Get the primary key columns
    return mapper.primary_key

    # return [pk.name for pk in primary_keys]
    # # Print the primary key columns
    # for pk in primary_keys:
    #     print(f"Primary Key: {pk.name}")

def read(session, model, **filters):
    # geometry_columns = get_geometry_columns(model)
    # columns = []
    # inspector = inspect(model)
    # for column in inspector.mapper.column_attrs:
    #     if isinstance(column.columns[0].type, Geometry):
    #         # Apply ST_AsGeoJSON to geometry columns
    #         columns.append(ST_AsGeoJSON(column.columns[0]).label(column.key))
    #     else:
    #         # Include other columns as-is
    #         columns.append(column.columns[0])
        
    # query = session.query(*columns)
    query = session.query(model)
    
    for column, value in filters.items():
        if not hasattr(model,column):
            raise KeyError("Invalid filter key: '%s' not present in model %s " % (column, model.__name__))
        query = query.filter(getattr(model, column) == value)
    # TODO greater than/smaller than filters
    # TODO in filters

    results = query.all()
    return results
    # data = []
    # for row in results:
    #     row_dict = {}
    #     for col, value in zip(columns, row):
    #         row_dict[col.name] = value
    #     data.append(row_dict) # instantiate_model(model,row_dict))

    # return data

def update(session, model, filters : dict = {}, **update_fields) -> int:

    if not len(update_fields.keys()):
        raise ValueError("At least one update field must be set")

    geometry_columns = get_geometry_columns(model).keys()

    for column, value in update_fields.items():
        if not hasattr(model,column):
            raise KeyError("Invalid update key: '%s' not present in model %s " % (column, model.__name__))
        if column in geometry_columns and type(value) == dict:
            update_fields[column] = shape(value).wkt

    query = session.query(model)
    
    for column, value in filters.items():
        if not hasattr(model,column):
            raise KeyError("Invalid filter key: '%s' not present in model %s " % (column, model.__name__))
        query = query.filter(getattr(model, column) == value)
   
    updated_count = query.update(update_fields, synchronize_session="fetch")

    session.commit()
    return updated_count

def delete(session, model, skip_confirmation = False, **filters) -> list:

    query = session.query(model)
    
    for column, value in filters.items():
        if not hasattr(model,column):
            raise KeyError("Invalid filter key: '%s' not present in model %s " % (column, model.__name__))
        query = query.filter(getattr(model, column) == value)
    # TODO greater than/smaller than filters
    # TODO in filters

    results = query.all()
    if results:
        if not skip_confirmation:
            # Prompt user for confirmation
            confirm = input("Do you want to proceed with deletion of %d records? (yes/no): " % len(results)).strip().lower()
            if confirm not in {'yes', 'y'}:
                print("Deletion canceled.")
                return []
        for row in results:
            session.delete(row)
        session.commit()
    return results


def list_of_dict_to_geojson_feature_collection(data : List[dict], geometry_column : str) -> GeoJSON:
    return {
        "type" : "FeatureCollection",
        "features": [
            dict_to_geojson_feature(item, geometry_column)
            for item in data
        ]
    }

def dict_to_geojson_feature(item : dict, geometry_column : str) -> dict:
    if geometry_column not in item:
        raise ValueError("geometry column missing from item")
    return {
        "type": "Feature",
        "properties": {
            key: value
            for key, value in item.items() if key != geometry_column
        },
        "geometry": item[geometry_column]
    }

def wkb_to_geojson(wkb_element : WKBElement):
    # Convert WKB to Shapely geometry object
    geom = to_shape(wkb_element)
    # geom = wkb.loads(wkb_element)
    
    # Convert the Shapely geometry to GeoJSON
    geojson = geom.__geo_interface__  # This gives the GeoJSON representation
    return geojson

def wkt_to_geojson(value):
    return from_wkt(value).__geo_interface__

def column_to_geojson(value):
    if type(value) == str:
        return wkt_to_geojson(value)
    elif type(value) == WKBElement:
        return wkb_to_geojson(value)
    else:
        raise TypeError("Invalid type: %s" % type(value))

def models_to_geojson_dict(models : list, geometry_column : str = "geom") -> GeoJSON:
    return list_of_dict_to_geojson_feature_collection(
        models_to_dict(models, geometry_to_geojson=True),
        geometry_column = geometry_column
    )

def models_to_dict(models : list, geometry_to_geojson : bool = False) -> List[dict]:
    """Convert each model instance into its dict representation and return a list"""
    return [
        model.to_dict(geometry_to_geojson) for model in models
    ]

def model_to_dict(model_instance, geometry_to_geojson : bool = False, datetime_to_str : bool = False):
    """Convert a SQLAlchemy ORM instance to a dictionary, skipping relationships."""
    geometry_columns = model_instance.get_geometry_columns()
    mapper = class_mapper(model_instance.__class__)
    result = {}
    for attr in mapper.attrs:
        if isinstance(attr, ColumnProperty):  # Only include columns
            value = getattr(model_instance, attr.key)
            if geometry_to_geojson and attr.key in geometry_columns and value is not None:
                result[attr.key] = column_to_geojson(value)
            elif datetime_to_str and type(value) == datetime:
                result[attr.key] = value.isoformat()
            else:
                result[attr.key] = value
    return result


# def model_to_dict(model) -> dict:
#     mapper = class_mapper(model.__class__)
#     geometry_columns = model.get_geometry_columns()
#     return {
#         column.key: column_to_geojson(getattr(model, column.key))
#             if column.key in geometry_columns
#             else getattr(model, column.key)
#         for column in mapper.columns if hasattr(model, column.key)
#     }

def write_to_file(file_path : str, content, serialize_as_json : bool=False, indent : int=None):
    """
    Tries to open a file in write mode, optionally serializes content as JSON, and writes it.

    Args:
        file_path (str): The path to the file to write.
        content (Any): The content to write to the file. Must be serializable if serialize_as_json is True.
        serialize_as_json (bool): Whether to serialize the content as JSON.
        indent (int, optional): Indentation level for JSON formatting. None for compact JSON.

    Returns:
        str: Success message or error description.
    """
    try:
        if serialize_as_json:
            # Serialize content as JSON
            content = json.dumps(content, cls=CustomJSONEncoder, indent=indent)

        with open(file_path, 'w') as file:
            file.write(content)
        file.close()
        return
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to write to {file_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path} (possibly an invalid directory)")
    except OSError as e:
        raise OSError(f"OS error occurred: {e}")
    except TypeError as e:
        raise TypeError(f"Serialization error: {e}")
    
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict(True,True)
        return super().default(obj)
    
def validate_geojson(data):
    """
    Manually validates if the provided data is a valid GeoJSON structure.
    
    Args:
        data (dict): The GeoJSON object to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    required_keys = {"type"}
    valid_types = {
        "FeatureCollection", "Feature", 
        "Point", "LineString", "Polygon", 
        "MultiPoint", "MultiLineString", "MultiPolygon", "GeometryCollection"
    }

    # Check required keys
    if not isinstance(data, dict):
        return False
    if not required_keys.issubset(data.keys()):
        return False
    if data["type"] not in valid_types:
        return False

    # Validate specific GeoJSON types
    if data["type"] == "FeatureCollection":
        if "features" not in data or not isinstance(data["features"], list):
            return False
        for feature in data["features"]:
            if not validate_geojson(feature):
                return False
    elif data["type"] == "Feature":
        if "geometry" not in data or "properties" not in data:
            return False
        if not validate_geojson(data["geometry"]):
            return False
    elif data["type"] in {"Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"}:
        if "coordinates" not in data:
            return False

    return True
