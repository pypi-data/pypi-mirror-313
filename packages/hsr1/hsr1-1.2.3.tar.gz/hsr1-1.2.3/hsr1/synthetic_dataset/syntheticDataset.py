# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import uuid
import os
import importlib

import numpy as np
import pandas as pd

pvlib_imported = False

try:
    import pvlib
    pvlib_imported = True
except:
    print("pvlib was not successfully imported")

import hsr1
from hsr1.utils.spectrum import spectrumUtils

SCALING_FACTOR = 0.617

rand = np.random.default_rng()

class SyntheticDataset():
    def __init__(self):
        if not pvlib_imported:
            raise ImportError("pvlib is required to generate synthetic datasets")
    
    def __init__(self, spectral_func=None, 
                 start_date="2024-01-01 00:00:00+00:00", 
                 end_date="2024-01-02 00:00:00+00:00",
                 latitude=53.14,
                 longitude=-1.64,
                 altitude=40):
        
        
        if spectral_func is None:
            self.spectral_func = self.generate_spectral_data
        
        self.spectral_data = None
        self.system_data = None
        self.deployment_metadata = None
        self.accessory_data = None
        
        self.start_date = start_date
        self.end_date = end_date
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        
        self.dataseries_id = None
    
    def get_dfs(self):
        return [self.spectral_data, self.system_data, self.deployment_metadata, self.accessory_data]
    
    def generate_custom_column(self, table, column, function, *args, **kwargs):
        if table == "spectral_data":
            self.spectral_data[column] = function(self.spectral_data["pc_time_end_measurement"], 
                                                  *args, **kwargs)
        elif table == "system_data":
            self.system_data[column] = function(self.spectral_data["pc_time_end_measurement"], 
                                                *args, **kwargs)
        elif table == "accessory_data":
            self.accessory_data[column] = function(self.accessory_data["pc_time_end_measurement"], 
                                                   *args, **kwargs)
        
        elif table == "deployment_metadata":
            self.deployment_metadata[column] = function(*args, **kwargs)
            
        else:
            raise ValueError("table not found")
    
    def remove_rows(self, table, function, *args, **kwargs):
        if table == "spectral_data":
            self.spectral_data = self.spectral_data.loc[function(self.spectral_data["pc_time_end_measurement"], *args, **kwargs), :]
        if table == "system_data":
            self.system_data = self.system_data.loc[function(self.system_data["pc_time_end_measurement"], *args, **kwargs), :]
        if table == "accessory_data":
            self.accessory_data = self.accessory_data.loc[function(self.accessory_data["pc_time_end_measurement"], *args, **kwargs), :]

    def global_integral(self, timestamps):
        if self.system_data is None:
            raise ValueError("system_data is required, generate that first")
            
        
        
    
    def generate_spectral_data(self, period="min"):
        spectral_data = pd.DataFrame()
        
        spectral_data["pc_time_end_measurement"] = pd.date_range(self.start_date, self.end_date, freq=period).astype(str)
        num_readings = len(spectral_data)
        spectral_data["sample_id"] = self.generate_sample_ids(spectral_data["pc_time_end_measurement"])
        spectral_data["dataseries_id"] = self.generate_dataseries_id()
        spectral_data["global_spectrum"] = self.smarts_integral_data(spectral_data["pc_time_end_measurement"]).tobytes()
        spectral_data["diffuse_spectrum"] = self.smarts_integral_data(spectral_data["pc_time_end_measurement"]).tobytes()
        spectral_data["global_integral"] = pd.to_datetime(spectral_data["pc_time_end_measurement"]).dt.hour
        spectral_data["diffuse_integral"] = spectral_data["global_integral"]/2
        spectral_data["global_molar"] = spectral_data["global_integral"]
        spectral_data["diffuse_molar"] = spectral_data["diffuse_integral"]
        spectral_data["camera_temp"] = rand.normal(30, 0.1, num_readings)
        
        
        self.spectral_data = spectral_data
    
    def generate_system_data(self, period="min"):
        system_data = pd.DataFrame()
        
        system_data["pc_time_end_measurement"] = pd.date_range(self.start_date, self.end_date, freq=period).astype(str)
        system_data["gps_time"] = pd.to_datetime(system_data["pc_time_end_measurement"]).dt.tz_localize(None).astype(str)
        system_data["gps_status"] = "A"
        system_data["gps_latitude"] = self.latitude
        system_data["gps_longitude"] = self.longitude
        system_data["gps_altitude"] = 100
        system_data["pressure"] = 1000
        system_data["baro_temp"] = 25
        system_data["rh"] = 13
        system_data["rh_temp"] = 0.0
        system_data["dataseries_id"] = self.generate_dataseries_id()
        system_data["sample_id"] = self.generate_sample_ids(system_data["pc_time_end_measurement"])
        
        
        self.system_data = system_data
    
    
    def generate_system_data_accessory(self, accessory_data=None, spectral_timestamps=None, spectral_sample_ids=None):
        if accessory_data is None:
            accessory_data = self.accessory_data
        if spectral_timestamps is None:
            spectral_timestamps = self.spectral_data["pc_time_end_measurement"]
        if spectral_sample_ids is None:
            spectral_sample_ids = self.spectral_data["sample_id"]
        
        system_data = hsr1.utils.ReformatData().reformat_system_data_reformatted_accessory(accessory_data, spectral_timestamps, spectral_sample_ids)
        
        system_data["dataseries_id"] = self.generate_dataseries_id()
        system_data["sample_id"] = self.generate_sample_ids(system_data["pc_time_end_measurement"])
        
        self.system_data = system_data
        
        
    
    def generate_deployment_metadata(self, filepath):
        self.deployment_metadata = hsr1.utils.ReformatData().reformat_deployment_metadata(filepath)
        # self.deployment_metadata["default_elevation"] = str(self.altitude)
        # self.deployment_metadata["default_latitude"] = str(self.latitude)
        # self.deployment_metadata["default_longitude"] = str(self.longitude)
    
    def generate_accessory_data(self, period="min"):
        accessory_data = pd.DataFrame()
        
        accessory_data["pc_time_end_measurement"] = pd.date_range(self.start_date, self.end_date, freq=period).astype(str)
        
        num_readings = len(accessory_data)
        
        accessory_data["Clock_Error"] = 0.0
        accessory_data["Latitude"] = rand.normal(self.latitude, 0.1, num_readings)
        accessory_data["Longitude"] = rand.normal(self.longitude, 0.1, num_readings)
        accessory_data["Altitude"] = rand.normal(100.0, 0.1, num_readings)
        accessory_data["GPSAge"] = 0.0
        accessory_data["NSV"] = rand.normal(10.0, 0.1, num_readings).astype(int)
        accessory_data["GPSSpare"] = rand.normal(5.0, 0.1, num_readings)
        accessory_data["_15Vin"] = rand.normal(23000.0, 0.1, num_readings)
        accessory_data["_3VCAP"] = rand.normal(22000.0, 0.1, num_readings)
        accessory_data["HTRIn"] = rand.normal(50.0, 0.1, num_readings)
        accessory_data["Vcc"] = rand.normal(3300.0, 0.1, num_readings)
        accessory_data["VSpare"] = rand.normal(0.0, 0.1, num_readings)
        accessory_data["I_Tot"] = rand.normal(484.0, 0.1, num_readings)
        accessory_data["I_15VPC"] = rand.normal(200.0, 0.1, num_readings)
        accessory_data["I_15VCAM"] = rand.normal(100.0, 0.1, num_readings)
        accessory_data["I_5VPC"] = rand.normal(4.0, 0.1, num_readings)
        accessory_data["ISpare"] = 0.0
        accessory_data["T_CPU"] = rand.normal(30.0, 0.1, num_readings)
        accessory_data["T_Bezel"] = rand.normal(29.0, 0.1, num_readings)
        accessory_data["T_RH"] = 0.0
        accessory_data["T_Baro"] = rand.normal(27.0, 0.1, num_readings)
        accessory_data["RH"] = rand.normal(12.0, 0.1, num_readings)
        accessory_data["Pressure"] = rand.normal(900.0, 0.1, num_readings)
        accessory_data["IMU_Output_Type"] = 2.0
        accessory_data["Yaw"] = rand.normal(358.0, 0.1, num_readings)
        accessory_data["Roll"] = rand.normal(-1.62, 0.1, num_readings)
        accessory_data["Pitch"] = rand.normal(10.31, 0.1, num_readings)
        accessory_data["Q_W"] = 16314.0
        accessory_data["Q_X"] = -1476.0
        accessory_data["Q_Y"] = 219.0
        accessory_data["Q_Z"] = 217.0
        accessory_data["Acc_X"] = 0.02
        accessory_data["Acc_Y"] = -0.23
        accessory_data["Acc_Z"] = 0.06
        accessory_data["IMU1"] = 0.0
        accessory_data["IMU2"] = 0.0
        accessory_data["Control_flags"] = 130.0
        accessory_data["Control_flags2"] = 0.0
        accessory_data["StatusFlags"] = 6144.0
        accessory_data["Heater"] = 0.0
        accessory_data["MsgCount"] = 69.0
        accessory_data["RdgCount"] = 0.0
        accessory_data["Watchdog"] = 3590.0
        accessory_data["gps_time"] = pd.to_datetime(accessory_data["pc_time_end_measurement"]).dt.tz_localize(None).astype(str)
        accessory_data["cpu_time"] = pd.to_datetime(accessory_data["pc_time_end_measurement"]).dt.tz_localize(None).astype(str)
        accessory_data["dataseries_id"] = self.generate_dataseries_id()
        accessory_data["sample_id"] =  self.generate_sample_ids(accessory_data["pc_time_end_measurement"])
        
        self.accessory_data = accessory_data
    
    
    """
    ---------------------------------------------------------------------------
    individual column functions
    ---------------------------------------------------------------------------
    """
    
    
    def generate_sample_ids(self, timeseries):
        """must have spectral_data generated first"""
        new_sample_ids = pd.DataFrame()
        new_sample_ids["pc_time_end_measurement"] = timeseries
        
        
        if self.spectral_data is not None:
            new_sample_ids = new_sample_ids.merge(self.spectral_data[["pc_time_end_measurement", "sample_id"]], how="left", on="pc_time_end_measurement")
        
        if "sample_id" in new_sample_ids.columns:
            not_matched = pd.isnull(new_sample_ids["sample_id"])
            new_sample_ids.loc[not_matched, "sample_id"] = [str(uuid.uuid1()) for i in range(np.sum(not_matched))]
        else:
            new_sample_ids["sample_id"] = [str(uuid.uuid1()) for i in range(len(timeseries))]
        
        return new_sample_ids["sample_id"]
    
    def generate_dataseries_id(self):
        if self.dataseries_id is None:
            self.dataseries_id = str(uuid.uuid1())
        
        return self.dataseries_id
    
    def linear_integral(self, timeseries):
        return np.ones(len(timeseries))

    def dist_from_midday(self, timeseries):
        timeseries = pd.to_datetime(timeseries)
        mins = timeseries.dt.hour*60 + timeseries.dt.minute
        return 720-np.abs(mins-720)

    def pvlib_integral_static(self, timeseries, *args):
        location = pvlib.location.Location(self.latitude, 
                                           self.longitude, 
                                           altitude=self.altitude)
        integrals = location.get_clearsky(pd.DatetimeIndex(timeseries))
        data = integrals[["ghi", "dhi"]].values*SCALING_FACTOR
        
        return data
    
    def smarts_integral_data(self, timeseries, filepath=None):
        if filepath is None:
            res = importlib.resources.files("hsr1.data").joinpath("smarts.txt")
            file = importlib.resources.as_file(res)
            with file as f:
                filepath = f
        
        smarts_data = spectrumUtils.read_simple_file(filepath)
        
        return smarts_data*len(timeseries)
    
    def integral_hour_of_day(self, timeseries):
        timeseries = pd.to_datetime(timeseries)
        return np.array([timeseries.dt.hour*100, timeseries.dt.hour*50]).T
    
    def remove_n_hour(self, timeseries, hour):
        timestamps = pd.to_datetime(timeseries)
        return timestamps.dt.hour != hour
    
    def num_readings(self, timeseries, base=0, scale=1):
        data = [i for i in range(len(timeseries))]
        data = base + np.array(data)*scale
        return data
        
        
"""
GUIDE TO WRITING CUSTOM FUNCTIONS:

dataseries and timeseries is automatically passed in, so the function must expect it
return a list, np array or series of data for the specific column

use it with

dataseries.generate_custom_column(table, column, function, **kwargs)
"""





if __name__ == "__main__":
    db_name = "databases/synthetic.db"
    
    if os.path.exists(db_name):
        os.remove(db_name)
    
    latitude = 13.19
    longitude = -59.54
    altitude = 40
    
    synthetic_dataset = SyntheticDataset(start_date="2023-01-01 00:00:00+00:00", 
                                         end_date="2023-01-03 23:59:00+00:00",
                                         latitude=latitude, longitude=longitude,
                                         altitude=40)
    
    synthetic_dataset.generate_spectral_data("10s")
    synthetic_dataset.generate_system_data()
    synthetic_dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    synthetic_dataset.generate_accessory_data()
    
    synthetic_dataset.generate_custom_column("spectral_data", 
                                             ["global_integral", "diffuse_integral"], 
                                             synthetic_dataset.pvlib_integral_static)
    
    dfs = synthetic_dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    graph = hsr1.Graph(db)
    graph.plot_integral()
    graph.plot_accessory()
    graph.plot_gps()
    graph.plot_dips_summary()