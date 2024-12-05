 # -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import os
import xml.etree.ElementTree as ET

import pandas as pd
import warnings

##### supressing pandas performance warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


from hsr1.db import (
    SqliteDBLoad,
    SqliteDBStore,
    PreCalculations
)

from hsr1.utils.reformatData import ReformatData as reformat


class DBDriver:
    """Generic class for database operations.
    
    contains a load and a store object,
    also exposes common methods in those objects to the user for easy access
        e.g: driver.load rather than driver.db_load.load
    """
    def __init__(self, db_name:str, db_type:str="sqlite"):
        """
        params:
            db_name: name of the db. if the db dosent exist, it will be created
                when data is stored to it
        """
        self.db_name = db_name
        if self.db_name[-3:] != ".db":
            self.db_name += ".db"
        
        if db_type == "sqlite":
            self.db_store = SqliteDBStore(self)
            self.db_load = SqliteDBLoad(self.db_name)
        else:
            raise NotImplementedError("Only sqlite databases are currently supported")
    
    
    @property
    def last_timestamp(self) -> str:
        """returns a string of the last timestamp in the database, None if empty"""
        df = self.db_load.load_sql("SELECT pc_time_end_measurement FROM spectral_data ORDER BY pc_time_end_measurement DESC LIMIT 1")
        if df is None:
            return None
        return df.loc[0, 0] 
    
    @property
    def first_timestamp(self) -> str:
        """returns a string of the first timestamp in the database, None if empty"""
        df = self.db_load.load_sql("SELECT pc_time_end_measurement FROM spectral_data ORDER BY pc_time_end_measurement ASC LIMIT 1")
        if df is None:
            return None
        return df.loc[0, 0]
    
    ##### exposing some methods from store and load to make them easier to access
    ##### e.g: driver.load() rather than driver.load.load()
    def store(self, dfs:tuple, precalculate:bool=True):
        self.db_store.store(dfs, precalculate)
    
    def combine_database(self, new_db_name:str):
        self.db_store.combine_database(new_db_name)
    
    def combine_database_folder(self, folder, delete=False):
        self.db_store.combine_database_folder(folder, delete)
    
    def store_raw(self, dfs, deployment_metadata):
        self.db_store.store_raw(dfs, deployment_metadata)
    
    def load_table_names(self) -> pd.DataFrame:
        return self.db_load.load_table_names()
    
    def load_sql(self, sql:str) -> pd.DataFrame:
        return self.db_load.load_sql(sql)
    
    def load(self, columns:[str]=[], 
             table:str=None,
             start_time:str=None, 
             end_time:str=None,
             condition:str="",
             raise_on_missing:bool=True,
             sort:bool=True,
             deserialise:bool=True,
             timezone:str="+00:00"
             ) -> pd.DataFrame:
        return self.db_load.load(columns,
                                 table,
                                 start_time,
                                 end_time,
                                 condition,
                                 raise_on_missing,
                                 sort,
                                 deserialise,
                                 timezone)
    
    def load_accessory(self, columns:[str]=[], 
                       start_time:str=None, 
                       end_time:str=None,
                       condition:str="",
                       raise_on_missing:bool=True,
                       sort:bool=True,
                       timezone:str="+00:00"
                       ) -> pd.DataFrame:
        return self.db_load.load_accessory(columns,
                                           start_time,
                                           end_time,
                                           condition,
                                           raise_on_missing,
                                           sort,
                                           timezone)
    
    def load_metadata(self, columns:[str]=[], condition:str="",
                      raise_on_missing=True) -> pd.DataFrame:
        return self.db_load.load_metadata(columns, condition, raise_on_missing)
    
    def load_spectrum(self, column:str, 
             table:str=None,
             start_time:str=None, 
             end_time:str=None,
             condition:str="",
             raise_on_missing:bool=True,
             sort:bool=True,
             deserialise:bool=True,
             timezone:str="+00:00"
             ) -> pd.DataFrame:
        return self.db_load.load_spectrum(column,
                                          table,
                                          start_time,
                                          end_time,
                                          condition,
                                          raise_on_missing,
                                          sort,
                                          timezone)
    
    def load_raw(self, columns=[], start_time=None, end_time=None):
        return self.db_load.load_raw(columns, start_time, end_time)


    def exists(self) -> bool:
        ##### TODO: move somewhere, this is sqlite specific
        """checks if a database exists and has all columns, returns bool"""
        if not os.path.isfile(self.db_name):
            return False
        
        column_headings = self.db_load.load_table_names()
        if len(column_headings) > 0:
            return True
        else:
            return False
    
    
    def add_precalculated_values(self, method:str=None, mobile=True, sample_ids_to_add=None, drop_existing=True):
        """calculates some commonly used values and stores them to the database
        
        params:
            method: which library to use
                "ephem": basic calculation
                "sg2_static": really fast for a static instrument
                "sg2_mobile": slow, not reccomended, but works for a mobile dataset
                "sg2": detects wether the dataset is mobile and uses the appropriate method
                None(default): uses "sg2_static" if static, and ephem if mobile
            mobile: wether or not the dataset's location will change. if you know 
                it won't, you can pass mobile=False and calculations will be sped up
            sample_ids_to_add(np.array): array of sample ids that correspond to 
                the readings that precaclulated_values will be calculated for
            drop_existing: deletes the existing data in the database. default true
                as this function is usually used to recalculate a whole dataset.
                To fill in a gap or recalculate a small section and keep the rest,
                set this to False and pass in the sample ids you want to add
                
        no returns, just updates the database with a new table
        """
        ref = reformat()
        
        deployment_metadata = self.load_metadata()
        
        if sample_ids_to_add is None or len(sample_ids_to_add) == 0: 
            if drop_existing:
                sample_ids_to_add = self.db_load.load(["sample_id"], table="spectral_data")["sample_id"].values
            else:
                print("no sample_ids_to_add was provided and drop_existing=False, doing nothing")
                return
            
        
        if drop_existing:
            self.db_store.drop_table("precalculated_values")
        
        p_calcs = PreCalculations(deployment_metadata=deployment_metadata)
        spectral_data = self.db_load.load(["pc_time_end_measurement", "sample_id", "dataseries_id"], table="spectral_data")

        data = None
        try:
            data = self.db_load.load(p_calcs.requirements+["sample_id"])
            data = data.drop_duplicates(subset="sample_id", ignore_index=True)
        except KeyError:
            data = pd.DataFrame()
            data["pc_time_end_measurement"] = spectral_data["pc_time_end_measurement"]
        
        if "gps_longitude" not in data.columns:
            data["gps_longitude"] = deployment_metadata["default_longitude"].iloc[0]
            data["gps_latitude"] = deployment_metadata["default_latitude"].iloc[0]
            data["gps_altitude"] = deployment_metadata["default_elevation"].iloc[0]
        
        
        if sample_ids_to_add is not None:
            select_data = data.set_index("sample_id")
            data_to_calculate = select_data.loc[sample_ids_to_add, :]
            data_to_calculate["sample_id"] = data_to_calculate.index
            data = data_to_calculate.reset_index(drop=True)
        
        
        
        precalculated_values = p_calcs.calculate_all(data, method)
        
        precalculated_values = reformat().reset_index(precalculated_values, "pc_time_end_measurement")
        # TODO: this dosent work if dataseries_id changes - need to check the dataseries_id for each sample_id
        precalculated_values["dataseries_id"] = spectral_data["dataseries_id"]
        precalculated_values["sample_id"]  = sample_ids_to_add
        
        deployment_ids = {}
        timezones = {}
        timedeltas_series = precalculated_values["dataseries_id"].copy()
        for i in range(len(deployment_metadata)):
            deployment_id = deployment_metadata.loc[i, "deployment_id"]
            dataseries_id = deployment_metadata.loc[i, "dataseries_id"]
            deployment_ids[dataseries_id] = deployment_id
            
            timezone, timedelta = ref.calculate_timezone(deployment_metadata.loc[i, "timezone"])
            timezones[deployment_metadata.loc[i, "deployment_id"]] = timezone
            
            timedeltas_series[timedeltas_series == dataseries_id] = timedelta
        
        
        timezones_series = precalculated_values["dataseries_id"].replace(deployment_ids).replace(timezones)
        
        
        precalculated_values["pc_time_end_measurement"] = pd.to_datetime(precalculated_values["pc_time_end_measurement"], utc=True)
        precalculated_values["pc_time_end_measurement"] = (precalculated_values["pc_time_end_measurement"]+timedeltas_series).astype(str)
        precalculated_values["pc_time_end_measurement"] = precalculated_values["pc_time_end_measurement"].str.slice(stop=19)
        precalculated_values["pc_time_end_measurement"] = precalculated_values["pc_time_end_measurement"]+timezones_series
        
        ##### remove rows where data couldnt be calculated
        precalculated_values = precalculated_values.loc[~precalculated_values["sza"].isnull(), :]
        
        print("storing precalculated values")
        self.db_store.store_dataframe(precalculated_values, "precalculated_values")
    
    
    def make_gpx(self, filename:str):
        """make and save an .xml file
        
        can be used on google my maps or another gpx viewer
        
        params:
            filename: the file location that the .gpx file will be saved to
        
        """
        
        data = self.db_load.load(["pc_time_end_measurement", "gps_latitude", "gps_longitude", "gps_altitude"])
        
        ##### select the first reading from each hour
        data["pc_time_end_measurement"] = data["pc_time_end_measurement"].astype(str).str.slice(stop=13)
        data = data.ffill().bfill()
        data = data.groupby("pc_time_end_measurement").first()
        data = data.reset_index()
        data["pc_time_end_measurement"] = data["pc_time_end_measurement"].str.slice(stop=10) + "T" + data["pc_time_end_measurement"].str.slice(11) + ":00:00"
        
          
        ##### settings for the gpx(root) tag
        gpx = ET.Element("gpx")
        gpx.set("version", "1.1")
        gpx.set("creator", "Peak Design")
        
        ##### setting metadata
        metadata = ET.SubElement(gpx, "metadata")
        metadata.set("name", "hsr-1 location data")
        author = ET.SubElement(metadata, "author")
        author_name = ET.SubElement(author, "name")
        author_name.text = "Peak Design"
        
        ##### makes a track element that will contain all the track data
        trk = ET.SubElement(gpx, "trk")
        name = ET.SubElement(trk, "name")
        name.text = "HSR-1 gps data"
        trkseg = ET.SubElement(trk, "trkseg")
        
        for i in range(len(data)):
            ##### makes a new track point for each 
            trkpt = ET.SubElement(trkseg, "trkpt")
            trkpt.set("lat", str(data.loc[i, "gps_latitude"]))
            trkpt.set("lon", str(data.loc[i, "gps_longitude"]))
            trkpt.set("ele", str(data.loc[i, "gps_altitude"]))
            
            time = ET.SubElement(trkpt, "time")
            time.text = data.loc[i, "pc_time_end_measurement"]
        
        #####
        xml = ET.tostring(gpx)
        
        if filename[-4:] != ".gpx":
            filename += ".gpx"
        
        with open(filename, "wb") as f:
            f.write(xml)

    
            
            
