from a5py.a5_connection import Connection, a5_tables
from a5py.util import serialize_connection_string, validate_date, write_to_file
from a5py.config import config
from a5py import SerieRast
import argparse
import json
import os
import logging
from typing import Tuple

default_connection_dict = {**{option: config.get("db_params", option) for option in config.options("db_params")}, "protocol": "postgresql"}
default_connection_string = serialize_connection_string(default_connection_dict)

def parse_json(value):
    """
    Custom argparse type to handle JSON strings or JSON file paths.
    """
    # Check if the value is a path to an existing file
    if os.path.isfile(value):
        try:
            with open(value, 'r') as f:
                return json.load(f)  # Load JSON from file
        except Exception as e:
            raise argparse.ArgumentTypeError(f"Error reading JSON file: {e}")
    
    # Attempt to parse as a JSON string
    try:
        return json.loads(value)  # Parse JSON string
    except json.JSONDecodeError:
        raise argparse.ArgumentTypeError(f"Invalid JSON string or file path: {value}")


def valid_date(date_str):
    try:
        return validate_date(date_str)
    except ValueError as e:
        raise argparse.ArgumentTypeError(e)

def parse_key_value_pair(pair : str) -> Tuple[str, str]:
    """Parses a single key=value pair."""
    try:
        key, value = pair.split('=', 1)
        return key.strip(), value.strip()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid key-value pair: '{pair}'. Expected format is key=value.")


def run_create_tables(args):
    """
    url : str, serie : dict, force_recreate : bool = False
    """
    connection = Connection(url=args.url)

    if args.force_recreate:
        connection.drop_tables()
    
    connection.create_tables()

    if args.serie is not None:

        # populate series table
        connection.insert(SerieRast,args.serie,True)
    connection.session.close()

def run_drop_tables(args):
    """
    url : str, serie : dict, force_recreate : bool = False
    """
    connection = Connection(url=args.url)

    connection.drop_tables()
    connection.session.close()

def valid_serie(serie : str):
    try:
        return json.loads(serie)
    except json.JSONDecodeError as e:
        # Catch any JSON decoding errors
        raise json.JSONDecodeError("parámetro serie incorrecto. No se pudo convertir a json: %s" % str(e))   

def valid_a5_model(model):
    if model not in a5_tables:
        raise ValueError("el argumento <clase> no corresponde con una clase válida del esquema a5")
    return a5_tables[model]

def run_export(args):
    filters = {
        "timestart": args.timestart
    }
    connection = Connection(url=args.url)
    connection.observacion_rast_to_geotiff(filters,args.output)
    connection.session.close()

def run_create(args):
    connection = Connection(url=args.url)
    try:
        if args.model is None:
            if args.geojson:
                raise ValueError("argumento --geojson no permitido si no se suministra --model")
            for model_key, values in args.json_input.items():
                model = valid_a5_model(model_key)
                connection.create(model.__name__, values)
        else:
            connection.create(args.model.__name__, args.json_input, args.geojson)
    except Exception as e:
        logging.error("Ocurrió un error en la transacción")
        raise
    finally:
        connection.cleanup()

def run_read(args):
    filter_dict = dict(args.filter) if args.filter else {}
    connection = Connection(url=args.url)
    try:
        result = connection.read(args.model.__name__, geojson = args.geojson, filters = filter_dict)
        write_to_file(args.output, result, serialize_as_json=True, indent=4)
    except KeyError as e:
        logging.error(f"{e}")
        exit(3)
    except Exception as e:
        logging.error("Ocurrió un error en la transacción")
        exit(1)
    finally:
        connection.cleanup()

def run_update(args):
    filter_dict = dict(args.filter) if args.filter else {}
    update_fields_dict = dict(args.update_fields)
    connection = Connection(url=args.url)
    try:
        updated_count = connection.update(args.model.__name__, filters = filter_dict, update_fields = update_fields_dict)
    except KeyError as e:
        logging.error(f"{e}")
        exit(3)
    except Exception as e:
        logging.error("Ocurrió un error en la transacción")
        exit(1)
    finally:
        connection.cleanup()
    logging.info("updated count: %d" % updated_count)

def run_delete(args):
    filter_dict = dict(args.filter) if args.filter else {}
    connection = Connection(url=args.url)
    try:
        result = connection.delete(args.model.__name__, skip_confirmation=args.skip_confirmation, filters = filter_dict)
        if args.output is not None:
            write_to_file(args.output, result, serialize_as_json=True, indent=4)
    except KeyError as e:
        logging.error(f"{e}")
        exit(3)
    except Exception as e:
        logging.error("Ocurrió un error en la transacción")
        exit(1)
    finally:
        connection.cleanup()

def run_rast2areal(args):
    connection = Connection(url=args.url)
    try:
        connection.query_rast_2_areal(
            args.area_id, 
            args.rast_series_id, 
            args.timestart, 
            args.timeend, 
            agg_func = args.agg_func,
            areal_series_id = args.areal_series_id,
            insert = args.insert,
            on_conflict = args.on_conflict,
            output = args.output
        )
    except Exception as e:
        # logging.error(f"Ocurrió un error en la transacción: {e}")
        # exit(1)
        raise
    finally:
        connection.cleanup()

def main():    
    parser = argparse.ArgumentParser(description="Comandos para interactuar con la base de datos")

    subparsers = parser.add_subparsers(title="commands", dest="command", required=True)

    # create / drop schema

    create_tables_parser = subparsers.add_parser("create_tables", help="crea tablas para almacenamiento de observaciones raster")
    create_tables_parser.add_argument("-u","--url",type=str, help="URL de la base de datos (ejemplo: postgresql://username:password@localhost:5432/dbname)", default = default_connection_string)
    create_tables_parser.add_argument("-s","--serie",type=valid_serie, help='crear serie raster a partir de cadena de texto json (ejemplo: {"id": 19, "var_id": 30})')
    create_tables_parser.add_argument("--force-recreate",action="store_true", help="recrear tablas (drop tables before create)")
    create_tables_parser.set_defaults(func=run_create_tables)

    drop_tables_parser = subparsers.add_parser("drop_tables", help="elimina tablas para almacenamiento de observaciones raster")
    drop_tables_parser.add_argument("-u","--url",type=str, help="URL de la base de datos (ejemplo: postgresql://username:password@localhost:5432/dbname)", default = default_connection_string)
    drop_tables_parser.set_defaults(func=run_drop_tables)

    #   read / export

    export_parser = subparsers.add_parser("export", help="exporta observacion raster como archivo geotiff")
    export_parser.add_argument("timestart", type=valid_date, help="etiqueta temporal de la observacion a exportar YYYY-MM-DD")
    export_parser.add_argument("output", type=str, help="archivo de salida")
    export_parser.add_argument("-u","--url",type=str, help="URL de la base de datos (ejemplo: postgresql://username:password@localhost:5432/dbname)", default = default_connection_string)
    export_parser.set_defaults(func=run_export)

    # CRUD

    # create
    create_parser = subparsers.add_parser("create", help="Inserta objetos en base de datos a partir de archivo JSON")
    create_parser.add_argument(
        'json_input',
        type=parse_json,
        help="string JSON o ruta a un archivo JSON"
    )
    create_parser.add_argument("-m","--model", type=valid_a5_model, help="Modelo de los objetos a insertar. Opciones: %s. Si no se define, json_input debe ser tener como claves los nombres de las clases y como valores, arreglos de los objetos a crear. Si se define, json_input puede ser un arreglo de objetos o un único objeto" % a5_tables.keys())
    create_parser.add_argument("-u","--url",type=str, help="URL de la base de datos (ejemplo: postgresql://username:password@localhost:5432/dbname)", default = default_connection_string)
    create_parser.add_argument("-g","--geojson", action="store_true", help = "Indica que json_input es GeoJSON")
    create_parser.set_defaults(func=run_create)

    # read
    read_parser = subparsers.add_parser("read", help="Lee objetos de base de datos")
    read_parser.add_argument("model", type=valid_a5_model, help="Modelo de los objetos a leer. Opciones: %s." % a5_tables.keys())
    read_parser.add_argument("output", type=str, help="Archivo de salida")
    read_parser.add_argument("-u","--url",type=str, help="URL de la base de datos (ejemplo: postgresql://username:password@localhost:5432/dbname)", default = default_connection_string)
    read_parser.add_argument("-g","--geojson", action="store_true", help = "genera formato GeoJSON. Sólo válido para objetos con geometría")
    read_parser.add_argument("-f","--filter", type=parse_key_value_pair,action='append', help="Filtro en la forma clave=valor")
    read_parser.set_defaults(func=run_read)

    # update
    update_parser = subparsers.add_parser("update", help="Actualiza objetos de base de datos")
    update_parser.add_argument("model", type=valid_a5_model, help="Modelo de los objetos a actualizar. Opciones: %s." % a5_tables.keys())
    update_parser.add_argument("update_fields", type=parse_key_value_pair,action='append', help="Campo a actualizar en la forma clave=valor")
    # update_parser.add_argument("output", type=str, help="Archivo de salida")
    update_parser.add_argument("-u","--url",type=str, help="URL de la base de datos (ejemplo: postgresql://username:password@localhost:5432/dbname)", default = default_connection_string)
    # update_parser.add_argument("-g","--geojson", action="store_true", help = "genera formato GeoJSON. Sólo válido para objetos con geometría")
    update_parser.add_argument("-f","--filter", type=parse_key_value_pair,action='append', help="Filtro en la forma clave=valor")
    update_parser.set_defaults(func=run_update)

    # delete
    delete_parser = subparsers.add_parser("delete", help="Elimina objetos de base de datos")
    delete_parser.add_argument("model", type=valid_a5_model, help="Modelo de los objetos a eliminar. Opciones: %s." % a5_tables.keys())
    delete_parser.add_argument("-o","--output", type=str, help="Guardar los objetos eliminados en este archivo de salida")
    delete_parser.add_argument("-u","--url",type=str, help="URL de la base de datos (ejemplo: postgresql://username:password@localhost:5432/dbname)", default = default_connection_string)
    delete_parser.add_argument("-f","--filter", type=parse_key_value_pair,action='append', help="Filtro en la forma clave=valor")
    delete_parser.add_argument("-s","--skip_confirmation", action='store_true', help="Saltear confirmación (sí a todo)")
    delete_parser.set_defaults(func=run_delete)

    # RAST 2 AREAL

    rast2areal_parser = subparsers.add_parser("rast2areal", help="extrae serie areal a partir de serie raster")
    rast2areal_parser.add_argument("rast_series_id", type=int, help="Id de serie raster")
    rast2areal_parser.add_argument("area_id", type=int, help="Id de area")
    rast2areal_parser.add_argument("timestart", type=valid_date, help="Fecha inicial")
    rast2areal_parser.add_argument("timeend", type=valid_date, help="Fecha final")
    rast2areal_parser.add_argument("-a","--agg_func", type=str, help="Funcion", choices=["mean", "count", "sum", "stddev", "min", "max"])
    rast2areal_parser.add_argument("-s","--areal_series_id", type=int, help="id de serie areal a la cual asignar el resultado")
    rast2areal_parser.add_argument("-i","--insert", action="store_true", help="Inserta el resultado en la serie areal indicada con -s")
    rast2areal_parser.add_argument("-c","--on_conflict", type=str, help="Indica qué acción realizar si al insertar se encuentra un conflicto de clave primaria. Por defecto se genera un error",choices=["update","nothing"])
    rast2areal_parser.add_argument("-o","--output", type=str, help="Guardar la serie areal en este archivo de salida")
    rast2areal_parser.add_argument("-u","--url",type=str, help="URL de la base de datos (ejemplo: postgresql://username:password@localhost:5432/dbname)", default = default_connection_string)
    rast2areal_parser.set_defaults(func=run_rast2areal)

    # parse args

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()