# modis

## Instalación

    # instala dependencias
    sudo apt update
    sudo apt install postgresql postgresql-contrib gdal-bin python3-gdal libgdal-dev postgis postgresql-16-postgis-3

    # crea ambiente de python e instala
    python -m venv myenv
    source myenv/bin/activate
    pip install .

    # asigna variables de ambiente (editar de ser necesario)
    DBNAME=modis
    DBUSER=modis
    DBPASSWORD=modis
    DBHOST=localhost
    DBPORT=5432

    # crea base de datos (necesita loguearse como superusuario)
    createdb -h $DBHOST -p $DBPORT $DBNAME
    psql $DBNAME -c "CREATE USER $DBUSER WITH SUPERUSER PASSWORD '$DBPASSWORD';" -h $DBHOST -p $DBPORT 
    psql $DBNAME -c  "CREATE EXTENSION postgis" -h $DBHOST -p $DBPORT 
    psql $DBNAME -c  "CREATE EXTENSION postgis_raster" -h $DBHOST -p $DBPORT 
    psql $DBNAME -c "ALTER DATABASE $DBNAME SET postgis.gdal_enabled_drivers TO 'ENABLE_ALL';"
    sudo service postgresql restart

    # configura
    a5py_config
    nano $HOME/.a5py.ini

    # crea tablas
    a5py create_tables -u "postgresql://$DBUSER:$DBPASSWORD@$DBHOST:$DBPORT/$DBNAME"

## Configuración

    # genera archivo de configuración
    a5py_config
    # editar los parámetros de conexión a la base de datos (db_params) y otros parámetros
    nano $HOME/a5py.ini 

## Uso

    # create schema
    a5py create_tables -u postgresql://modis:modis@localhost:5432/a5_test
    # insert serie rast
    a5py create -m SerieRast '{"id":19, "fuentes_id":40}' -u postgresql://modis:modis@localhost:5432/a5_test
    # insert rast
    python we2db.py -r $HOME/modis/output -D postgresql://modis:modis@localhost:5432/a5_test -o /tmp/inserted_rast.json -i 19
    # insert area
    a5py create -m Area $HOME/Downloads/area_138.json -g -u postgresql://modis:modis@localhost:5432/a5_test
    # insert serie areal
    a5py create -m SerieAreal '{"id":1,"area_id":138, "var_id": 30, "proc_id": 5, "unit_id": 14, "fuentes_id": 40, "nombre:"Picasa - we"}' -u postgresql://modis:modis@localhost:5432/a5_test
    # rast2areal
    a5py rast2areal 19 138 2009-01-25 2009-02-10 -a mean -i -s 1 -o /tmp/obs_areal.json -u postgresql://modis:modis@localhost:5432/a5_test
    # exporta raster de base de datos a geotiff
    a5py export 2009-02-10 modis_we_20090210.tif

## Todos los comandos y sus opciones

## TODO
- import gdal
