from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from osgeo import gdal
from datetime import datetime
from typing import List, Union
import logging

from .util.util import readGeoJson, readJson, insert, upsert, model_to_dict, read, get_geometry_columns, GeoJSON, models_to_geojson_dict, update, delete, write_to_file
from .a5_tables.base import Base
from .a5_tables import Area, SerieAreal, SerieRast, ObservacionAreal, ObservacionRast

a5_tables = {
    "Area": Area,
    "SerieAreal": SerieAreal,
    "SerieRast": SerieRast,
    "ObservacionAreal": ObservacionAreal,
    "ObservacionRast": ObservacionRast
}

gdal.UseExceptions()

class Connection():
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(url = url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def cleanup(self):
        self.session.rollback()
        self.session.close()
    
    def reopen(self):
        if self.session.is_active:
            self.cleanup()
        self.session = self.Session()

    def __del__(self):
        self.cleanup()

    def create_tables(self):
        # Create all tables in the database (this will create the 'observaciones_rast' table)
        print("Creating tables...")
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        print("Dropping tables...")
        Base.metadata.drop_all(self.engine)

    def insert(self,model : type,values : Union[dict,list],on_conflict_do_nothing : bool = False, returning : bool = False):
        return insert(self.session, model, values, on_conflict_do_nothing, returning)
        
    def upsert(self, model : type, values : list, returning : bool):
        return upsert(self.session, model, values, returning) 

    def query_with_filter(self,model : type, filters : dict):

        query = self.session.query(model)
        for attr, value in filters.items():
            query = query.filter(getattr(ObservacionRast, attr) == value)
        return query.all()

    def query_observaciones_rast(self,filters : dict):
        query = self.session.query(
            ObservacionRast.id,
            ObservacionRast.timestart,
            ObservacionRast.timeend,
            func.ST_AsGDALRaster(ObservacionRast.valor, 'GTiff').label('valor'),
            ObservacionRast.timeupdate,
            ObservacionRast.validada
        )
        for attr, value in filters.items():
            query = query.filter(getattr(ObservacionRast, attr) == value)
        return query.all()

    def observacion_rast_to_geotiff(self,filters : dict,output_filename : str):

        # observaciones = self.query_with_filter(ObservacionRast, filters)
        observaciones = self.query_observaciones_rast(filters)            
        
        if not len(observaciones):
            raise Exception("No se encontró observacion raster con el filtro suministrado")
        
        # Extract the raster data (in binary form)
        raster_data = observaciones[0].valor

        try:
            with open(output_filename, 'wb') as file:
                file.write(raster_data)
                file.flush()
                print("Bytes written to file successfully.")
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")
            raise e

        # Write the raster data to a GeoTIFF file using GDAL
        # Create an in-memory file-like object from the binary data
        # in_memory_file = io.BytesIO(raster_data)

        # Open the raster data with GDAL (this assumes the raster data is in a supported format like PNG or GeoTIFF)
        dataset = gdal.Open(output_filename)

        if dataset is None:
            raise Exception(f"Error: Unable to open raster data.")

        # Create the GeoTIFF output file
        # driver = gdal.GetDriverByName('GTiff')
        # output_dataset = driver.Create(output_filename, dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount, dataset.GetRasterDataType())

        # # Copy all the raster bands from the input dataset to the output dataset
        # for band_index in range(1, dataset.RasterCount + 1):
        #     band = dataset.GetRasterBand(band_index)
        #     output_band = output_dataset.GetRasterBand(band_index)
        #     output_band.WriteArray(band.ReadAsArray())

        # # Copy the spatial reference system (SRS), geotransform, and other metadata if available
        # output_dataset.SetGeoTransform(dataset.GetGeoTransform())
        # output_dataset.SetProjection(dataset.GetProjection())

        # # Flush the data to disk
        # output_dataset.FlushCache()

        print(f"GeoTIFF file written to {output_filename}")

    def query_rast_2_areal(
        self, 
        area_id : int, 
        rast_series_id : int, 
        timestart : datetime, 
        timeend : datetime, 
        agg_func : str = "mean",
        areal_series_id : int = None,
        insert : bool = False,
        on_conflict : str = "update",
        output : str = None
        ) -> list[ObservacionAreal]:
        """
            Clip raster timeseries with area and extract areal mean (or count, sum, stddev, min, max)

            Parameters:
            area_id (int): identifier of the area 

            rast_series_id (int): identifier of the raster series 

            timestart (datetime): begin timestamp

            timeend (datetime): end timestamp

            agg_func (str): the statistic function to extract from the clipped rasters. Options:
                - 'mean'
                - 'count'
                - 'sum'
                - 'stddev'
                - 'min'
                - 'max'

            areal_series_id (int): identifier of the resulting areal series 
            
            insert (bool) = False: option to insert ObservacionesAreales into the database
            
            on_conflict (str): Action to perform on unique key (series_id, timestart, timeend) conflict when creating ObservacionesAreales. Options:
                - None (default): raises an error
                - 'nothing': does nothing
                - 'update': updates valor and timeupdate fields

        """
        valid_agg_func = ["count", "sum", "mean", "stddev", "min", "max"]
        if agg_func not in valid_agg_func:
            raise ValueError("agg_func must be one of %s" % valid_agg_func)

        area = self.session.query(Area).get(area_id)

        # Query to compute the areal mean for a raster time series
        upserted = self.session.query(
            ObservacionRast.timestart,
            ObservacionRast.timeend,
            func.ST_SummaryStats(
                func.ST_Clip(ObservacionRast.valor, area.geom)
            ).label("stats")
        ).filter(
            ObservacionRast.series_id == rast_series_id,
            ObservacionRast.timestart >= timestart, 
            ObservacionRast.timestart <= timeend
        ).all()

        # Process the results
        observaciones = []
        for obs_timestart, obs_timeend, stats in upserted:
            if stats:
                stats = stats.strip("()").split(",")
                valor = stats[valid_agg_func.index(agg_func)]  # ST_SummaryStats returns [count, sum, mean, stddev, min, max]
                observaciones.append(
                    {
                        "series_id": areal_series_id,
                        "timestart": obs_timestart,
                        "timeend": obs_timeend,
                        "valor": float(valor)
                    }
                )
            else:
                print(f"Timestamp: {obs_timestart}, No overlap with polygon.")
        
        if areal_series_id is not None and insert:
            stmt = pg_insert(ObservacionAreal).values(observaciones)
            if on_conflict is not None:
                if on_conflict == "nothing":
                    stmt.on_conflict_do_nothing()
                elif on_conflict == "update":
                    stmt.on_conflict_do_update(
                        index_elements=["series_id", "timestart", "timeend"],
                        set_={"timeupdate":stmt.excluded.timeupdate, "valor":stmt.excluded.valor}
                    )
                else:
                    raise ValueError("Invalid on_conflict argument. Must be one of None, 'nothing', 'update'")
            stmt = stmt.returning(ObservacionAreal.id, ObservacionAreal.timestart, ObservacionAreal.timeend, ObservacionAreal.series_id, ObservacionAreal.valor, ObservacionAreal.timeupdate, ObservacionAreal.validada)
            upserted = self.session.execute(stmt)
            self.session.commit()
            result = upserted.fetchall()     
            if output is not None:
                write_to_file(output, [ObservacionAreal(**row._asdict()) for row in result], serialize_as_json=True, indent = 4)
            return result
        else:
            result = [
                ObservacionAreal(
                    **observacion
                ) for observacion in observaciones
            ]
            if output is not None:
                write_to_file(output, result, serialize_as_json=True, indent = 4)
            return result
        
    def create(self, model : str, data : Union[List[dict],dict,str], geojson : bool = False, on_conflict : str = None, returning : bool = False) -> list:
        """Insert instances of model

        Args:
            model (str): _description_
            data (Union[List[dict],dict,str]): _description_
            geojson (bool, optional): _description_. Defaults to False.
            on_conflict (str, optional): Action to perform on unique key conflict. Options:
                - None (default): raises an error
                - 'nothing': does nothing
                - 'update': updates excluded values.
            returning (bool): if True, return the created items

        Raises:
            ValueError: _description_

        Returns:
            list: _description_
        """
        if model not in a5_tables:
            raise ValueError("Model not in a5_tables")
        
        Model = a5_tables[model]
        
        if geojson:
            new_entries = readGeoJson(Model, data)
        else:
            new_entries = readJson(Model, data)

        # convert to dict
        new_entries = [ model_to_dict(entry) for entry in new_entries]

        if on_conflict == "update":
            results = self.upsert(Model, new_entries, returning)
        else:
            results = self.insert(Model, new_entries, (on_conflict == "nothing"), returning)
        return results

    def read(self, model : str, geojson : bool = False, filters : dict = {}, **more_filters) -> Union[list, GeoJSON]:
        
        if model not in a5_tables:
            raise ValueError("Model not in a5_tables")
        
        Model = a5_tables[model]

        for k, v in filters.items():
            if k in more_filters:
                raise ValueError("key %s of filter is duplicated in more_filters" % k)

        # retrieve model instances
        try:
            results = read(self.session, Model, **filters, **more_filters)
        except KeyError as e:
            raise

        if geojson:
            geometry_columns = get_geometry_columns(Model)
            if not len(geometry_columns.keys()):
                raise ValueError("This is not a geometry table. Can´t return geoJSON")
            return models_to_geojson_dict(results, list(geometry_columns.keys())[0]) # list_of_dict_to_geojson_feature_collection(results, geometry_columns.keys()[0])
        else:
            return results
    
    def update(self, model : str, filters : dict = {}, update_fields : dict = {}, **more_update_fields) -> int:
        if model not in a5_tables:
            raise ValueError("Model not in a5_tables")
        
        Model = a5_tables[model]

        for k, v in update_fields.items():
            if k in more_update_fields:
                raise ValueError("key %s of update_fields is duplicated in more_update_fields" % k)

        try:
            updated_count = update(session=self.session, model=Model, filters=filters, **update_fields, **more_update_fields)
        except KeyError as e:
            raise
        return updated_count
    
    def delete(self, model : str, skip_confirmation : bool = False, filters : dict = {}, **more_filters) -> list:

        if model not in a5_tables:
            raise ValueError("Model not in a5_tables")
        
        Model = a5_tables[model]

        for k, v in filters.items():
            if k in more_filters:
                raise ValueError("key %s of filter is duplicated in more_filters" % k)

        # retrieve model instances
        try:
            results = delete(session = self.session, model = Model, skip_confirmation=skip_confirmation, **filters, **more_filters)
        except KeyError as e:
            raise

        return results
