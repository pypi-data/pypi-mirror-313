# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import math

sg2_imported = False
try:
    import sg2
    sg2_imported = True
except Exception as e:
    print(e)

import ephem

import hsr1.utils.HSRFunc as HsrFunc


class PreCalculations:
    def __init__(self, deployment_metadata):
        self.deployment_metadata=deployment_metadata
        
        self.requirements = ["gps_longitude", "gps_latitude", "gps_altitude", "pressure", "baro_temp", "pc_time_end_measurement", "dataseries_id"]
        self.sun_data = None
        self.sg2_values = ["topoc.gamma_S0", "topoc.alpha_S", "topoc.toa_hi", "geoc.R"]
    
    
    
    
    def __calculate_raw_sg2_static(self, data):
        location = [data[col].mean() for col in ["gps_longitude", "gps_latitude", "gps_altitude"]]
        
        datetimes = data.index.tz_localize(None).astype("datetime64[ns]")
        
        sun_position = sg2.sun_position([location], datetimes, self.sg2_values)
        
        result = {}
        result["elevation"] = sun_position.topoc.gamma_S0[0]
        result["azimuth"] = sun_position.topoc.alpha_S[0]
        result["toa_hi"] = sun_position.topoc.toa_hi[0]
        result["sed"] = sun_position.geoc.R
        
        result["elevation"] = self.atmospheric_correction(result["elevation"])
        
        return result
        
    
    
    def __calculate_raw_sg2_mobile(self, data):        
        locations = data[["gps_longitude", "gps_latitude", "gps_altitude"]].values

        sun_position = [sg2.sun_position([locations[i]], [pd.to_datetime(data.index[i]).to_datetime64()], self.sg2_values) for i in range(len(data))]
        
        result = {}
        result["elevation"] = [sun.topoc.gamma_S0[0][0] for sun in sun_position]
        result["azimuth"] = [sun.topoc.alpha_S[0][0] for sun in sun_position]
        result["toa_hi"] = [sun.topoc.toa_hi[0][0] for sun in sun_position]
        result["sed"] = [sun.geoc.R[0] for sun in sun_position]
        
        result["elevation"] = self.atmospheric_correction(result["elevation"])
        
        return result
    
    def __calculate_raw_ephem(self, data):
        instrument = ephem.Observer()
        sun = ephem.Sun()
        static_sun = ephem.Sun()
        
        locations = data[["gps_longitude", "gps_latitude", "gps_altitude"]].values
        dates = data.index.tz_localize(None)
        
        result = {}
        result["elevation"] = []
        result["azimuth"] = []
        result["sed"] = []
        
        for i in range(len(data)):
            current_loc = locations[i]
            
            instrument.lon = str(current_loc[0])
            instrument.lat = str(current_loc[1])
            instrument.elevation = current_loc[2]
            instrument.date = str(dates[i])
            
            sun.compute(instrument)
            
            static_sun.compute(str(dates[i]))
            
            result["elevation"].append(sun.alt)
            result["azimuth"].append(sun.az)
            result["sed"].append(static_sun.earth_distance)
        
        result_df = pd.DataFrame(result)
        
        day_times = result_df["elevation"] > 0
        solar_constant = 1367
        toa_ni = solar_constant/(result_df["sed"]**2)
        result_df["toa_hi"] = 0.0
        result_df.loc[day_times, "toa_hi"] = toa_ni[day_times]*np.sin(result_df.loc[day_times, "elevation"])
        
        result["toa_hi"] = result_df["toa_hi"].to_numpy()
        
        return result
            

    
    def calculate_all(self, data, method=None):
        """calculates all the precalculated values

        returns a dataframe with them all in as columns
        """
        
        
        if method is None:
            method = "ephem"
        
        if method in ["sg2", "sg2_static"] and not sg2_imported:
            print("sg2 was not sucessfully imported, using ephem")
            method = "ephem"
        
        
        ##### use sg2 static unless sg2 mobile is specified
        if method == "sg2":
            method = "sg2_static"
        
        data = data.set_index("pc_time_end_measurement")
        data = data.replace({None:"nan"})
        data = data.astype(str)
        data = data.replace({"":"nan"})
        
        float_cols = [col for col in data.columns if col not in ["dataseries_id", "sample_id"]]
        data[float_cols] = data[float_cols].astype(float)
        
        gps_col_dict = {"default_latitude":"gps_latitude", 
                        "default_longitude":"gps_longitude",
                        "default_elevation":"gps_altitude"}
        
        for idx in self.deployment_metadata.index:
            deployment_row = self.deployment_metadata.loc[idx, :]
            this_dataseries = data["dataseries_id"]==deployment_row["dataseries_id"]
            for col in gps_col_dict:
                sys_col = gps_col_dict[col]
                if deployment_row[col] != "''":
                    nan_values = np.logical_and(this_dataseries, data[sys_col].isnull())
                    data.loc[nan_values, sys_col] = float(deployment_row[col])
                
            
        
        self.data = data
        
        if method == "sg2_mobile":
            self.sun_data = self.__calculate_raw_sg2_mobile(data)
        elif method == "ephem":
            self.sun_data = self.__calculate_raw_ephem(data)
        elif method == "sg2_static":
            self.sun_data = self.__calculate_raw_sg2_static(data)
        else:
            raise ValueError(method+"is an invalid library to use")
        
        
        
        
        
        self.precalculated_values = pd.DataFrame()
        self.precalculated_values.index = self.data.index
        
        self.precalculated_values["sza"] = self.sza(data)
        self.precalculated_values["azimuth"] = self.azimuth()
        self.precalculated_values["toa_hi"] = self.top_of_atmosphere_hi()
        self.precalculated_values["sed"] = self.sun_earth_distance()
        self.precalculated_values["airmass"] = self.airmass(data)
        
        
        
        return self.precalculated_values
    
    
    def atmospheric_correction(self, elv):
        """corrects a list of elevation values for atmospheric refration
        converts from absolute position to apparent position
        """
        
        if not sg2_imported:
            raise ImportError("SG2 was not successfully imported")
        
        pressure = 1013.25
        temperature = 25
        
        elv_corr = sg2.topocentric_correction_refraction_SAE(elv, pressure, temperature)
        
        return elv_corr
    
    
    def sza(self, df):
        """unpacks the elevation and corrects it for atmospheric refraction
        returns: nparray of solar zenith angles
        
        uses pressure and temperature values from internal sensors, forward fills if there are missing values
        """
        
        sza = (math.pi/2) - np.array(self.sun_data["elevation"])
        return sza
    
    def azimuth(self):
        """unpacks the azimuth value from sg2"""
        azi = self.sun_data["azimuth"]
        return azi
    
    def top_of_atmosphere_hi(self):
        """unpacks the top of atmosphere value from sg2"""
        toa = np.array(self.sun_data["toa_hi"])
        ##### adjusted because hsr1 only measures part of the spectrum
        return toa*(844/1367)
    
    def sun_earth_distance(self):
        """unpacks the sun earth distance value from sg2"""
        sed = self.sun_data["sed"]
        return sed
    
    def atmospheric_distance(self):
        """calculates the height of atmosphere that sun will travel through
        unneccessary, as earth is so much bigger than the atmosphere, this approaches parralel lines,
        can just use 1/cos(sza)
        """
        ##### TODO: use hsr_func's airmass function
            
        ##### radius of earth
        Re = 6371000
        
        ##### radius of atmosphere
        ##### very variable depending on what you want, should it be just as a ratio to atmospheric height?
        ##### if so then just set Ra to 1
        Ra = 1
        
        # solar zenith angle
        sza = self.precalculated_values["sza"]
        
        const = math.pow(Re, 2) + 2*Re*Ra + math.pow(Ra, 2)
        
        atmospheric_distance = np.sqrt(const - np.power(Re*np.sin(sza), 2)) - Re*np.cos(sza)
        
        return atmospheric_distance
    
    def cos_atmospheric_distance(self):
        Ra = 1
        sza = self.precalculated_values["sza"]
        return Ra/np.cos(sza)
        
    def airmass(self, df):
        data = pd.DataFrame()
        data["pressure"] = 1.01325
        data["sza"] = self.precalculated_values["sza"]
        daytimes = data["sza"] < 90
        data["airmass"] = np.nan
        data.loc[daytimes, "airmass"] = [HsrFunc.calc_air_mass(row[1]["sza"]) for row in data[daytimes].iterrows()]
    
        return data["airmass"]
































