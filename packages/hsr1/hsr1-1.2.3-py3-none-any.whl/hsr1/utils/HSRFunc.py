# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import os
import datetime as dt
import time
import importlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import matplotlib.dates as mdates
import ephem
import scipy.interpolate as interpolate
import zipfile





def calc_direct_normal_spectrum(global_spectrum, diffuse_spectrum, sza):
    """calculates the direct normal spectrum from the diffuse, global and zenith angle
    params:
        global_spectrum, diffuse_spectrum: either pandas Series of numpy arrays, each array representing one spectral reading
                                                  or dataframe with one row per wavelength reading
        sza: pandas Series one float(radians) per reading
    """
    direct_horizontal_spectrum = global_spectrum-diffuse_spectrum
    direct_normal_spectrum = direct_horizontal_spectrum/np.cos(sza)
    
    return direct_normal_spectrum
    

def calc_sun_zenith(ts, lat, lon):
    """calculates the solar zenith angle at a specific time and location
    quite slow as this has to be run in a for loop, sg2's calculation is much faster
    params:
        ts: timestamp that you want to measure, string yyyy-mm-dd hh:mm:ss
        lat, lon: latitude and longitude of the location
    
    returns:
        tuple of zenith angle and azimuth, in radians
    """
    obs = ephem.Observer()
    sun = ephem.Sun()

    obs.date = ts
    obs.lat, obs.lon = str(lat), str(lon)

    sun.compute(obs)

    return np.pi/2 - sun.alt, sun.az

def calc_rayleigh(wl, pressure = 1013.25):
    """calculates the rayleigh scattering
    params:
        wl: the wavelength(s) to calculate the scattering over.
            this can be a scalar, numpy array or pandas series
        pressure: the pressure in hPa
    return is in the same datatype as the wl parameter
    """
    a1 = 117.25942 # model Rayleigh scattering 
    a2 = -1.3215
    a3 = 0.00032073
    a4 = -0.000076842
    p0 = 1013.25 
    wl  = wl*1e-3 # convert wl from nano to micrometres (for Rayleigh formula)    
    tau_r = (pressure/p0)*(1/(a1*wl**4 + a2*wl**2 + a3 + a4/wl**2))
    return tau_r

def calc_air_mass(Sza, pressure=1013.25):
    """calculates the airmass
    params:
        Sza: the solar zenith angle in radians.
            this can be a scalar, numpy array or pandas series.
        pressure: the pressure in hPa
    return is in the same datatype as the wl parameter
    """
    a = 0.50572 
    b = 96.07995
    c = 1.6364
    C = np.cos(Sza)
    
    with np.errstate(divide="ignore", invalid="ignore"):
        mu = C + a*(b - np.degrees(Sza))**(-c) # atm. air mass (note 1/m in Wood et. al 2019)
    return pressure / 1013.25 / mu

def calc_aot_direct(ed, eds, sza, e_solar=None, sed=None, aod_type=["total_od", "aod_microtops", "aod_wood_2017"], et_wavelengths=None):
    """calculates the atmospheric optical depth in several different ways
    
    params:
        ed: the global spectral irradiance. columns=wavelength, index=time, timestamp in utc
        eds: the diffuse spectral irradiance. columns=wavelength, index=time, timestamp in utc
        sza: the solar zenith angle in radians. column = "sza"
        e_solar: the extraterrestrial solar spectrum. columns=wavelength, index=time, timestamp in utc
        sed: sun earth distance in AU, pandas Series. if None, calculated from time. this is quite slow so this parameter
            can speed it up if you are already loading from the database
        aod_type: the desired outputs string or list of strings
        
    
    returns:
        aod_data: dataframe containing all the requested aod_types
        to convert a column of numpy arrays into a dataframe of wavelengths against time:
            pd.DataFrame(np.stack(data["spectrum_column"].values), columns = np.arange(300, 1101, 1), index=data["pc_time_end_measurement"])
    
    definition of each aod type:
        tau_t/total_od: the total optical depth from all sources
        tau_a/microtops_aod: the aerosol optical depth. this is the optical depth with rayleigh scattering removed
        tau_corr/aod_wood_2017: the aerosol optical depth with an empirical correction applied to it
    """
    if e_solar is None:
        e_solar = load_et_spectrum(wavelengths=et_wavelengths)
    
    
    edd = (ed - eds)
    
    edni = edd.divide(np.cos(sza.values.astype(float)), axis="index")
    
    sun = ephem.Sun()
    
    tau_r = calc_rayleigh(ed.columns.astype(float))
    tau_t = np.nan*np.ones([len(edni),len(edni.T)]) # total OT 
    tau_a = np.nan*np.ones([len(edni),len(edni.T)]) # aerosol OT 
    tau_corr = np.nan*np.ones([len(edni),len(edni.T)]) # corrected OT
    
    wl_e = np.array([440, 500, 675, 870, 1020]) #  empirical correction coefficients (Wood 2017)
    offset_am = np.array([0.0097, 0.0177, -0.0033, -0.0067, -0.0117])
    offset_wl = np.array([0.0244, 0.0260, 0.0182, 0.0124, 0.0457])
    slope_wl = np.array([1.2701, 1.2893, 1.3549, 1.4522, 1.5237])
    
    wl = ed.columns.astype(float)
    offset_am = interpolate.interp1d(wl_e, offset_am, kind = 'linear', axis = 0, fill_value = "extrapolate") # interpolate to wl range of hsr (piecewise linear)
    offset_wl = interpolate.interp1d(wl_e, offset_wl, kind = 'linear', axis = 0, fill_value = "extrapolate")(wl) # linearly extrapolated outside wl range
    slope_wl = interpolate.interp1d(wl_e, slope_wl, kind = 'linear', axis = 0, fill_value = "extrapolate")(wl)
    
    daytime = sza.values < np.radians(90)
    daytime = daytime[:, 0]
    
    
    
    if sed is None:
        sed = np.full(len(edni), np.nan)
        for i in range(len(edni)):
            if sza.iloc[i].values < np.radians(90):
                sun.compute(edni.index[i])
                sed[i] = sun.earth_distance
        sed = pd.Series(sed)
    
    ##### vectorised calculations
    airmasses = calc_air_mass(sza).values[:, 0]
    
    e_toa = pd.DataFrame((e_solar.values/np.array([sed.values]).T**2), columns=e_solar.columns, index=ed.index)
    
    airmasses = airmasses.T[:, np.newaxis]
    offsets = offset_am(airmasses)
    
    dnitoa =edni.divide(e_toa).astype(float)
    
    ##### ignores divide by zero warnings. the values are returned as nan, and not plotted
    with np.errstate(divide="ignore", invalid="ignore"):
        tau_t = -1/airmasses*np.log(dnitoa)
    tau_a = tau_t-tau_r.values
    tau_corr = (tau_a - offsets - offset_wl) *slope_wl
    
    tau_t[np.logical_not(daytime)] = np.nan
    tau_a[np.logical_not(daytime)] = np.nan
    tau_corr[np.logical_not(daytime)] = np.nan
    
    aod_data = pd.DataFrame()
    aod_data["pc_time_end_measurement"] = ed.index
    
    if isinstance(aod_type, str):
        aod_type = [aod_type]
    
    if "total_od" in aod_type:
        aod_data["total_od"] = list(tau_t.values)
    if "aod_microtops" in aod_type:
        aod_data["aod_microtops"] = list(tau_a.values)
    if "aod_wood_2017" in aod_type:
        aod_data["aod_wood_2017"] = list(tau_corr.values)
    
    return aod_data


def calc_cimel_band_aot_direct(Ed, Eds, Sza, E_solar, sed, aod_type=["total_od", "aod_microtops", "aod_wood_2017"]):
    """calculates the AOD values at several wavelengths, that are also measured by cimel instruments
    
    params:
        ed: the global spectral irradiance. columns=wavelength, index=time, timestamp in utc
        eds: the diffuse spectral irradiance. columns=wavelength, index=time, timestamp in utc
        sza: the solar zenith angle in radians. column = "sza", index=time, timestamp in utc
        e_solar: the extraterrestrial solar spectrum. columns=wavelength, index=time, timestamp in utc
        sed: sun earth distance in AU. if None, calculated from time. this is quite slow so this parameter
            can speed it up if you are already loading from the database
        aod_type: the desired outputs string or list of strings
        
    
    returns:
        aod_data: dataframe containing all the requested channels
        to convert a column of numpy arrays into a dataframe of wavelengths against time:
            pd.DataFrame(np.stack(data["spectrum_column"].values), columns = np.arange(300, 1101, 1), index=data["pc_time_end_measurement"])
    
    definition of each aod type:
        tau_t/total_od: the total optical depth from all sources
        tau_a/microtops_aod: the aerosol optical depth. this is the optical depth with rayleigh scattering removed
        tau_corr/aod_wood_2017: the aerosol optical depth with an empirical correction applied to it
    """
    
    cimel_band = [380, 440, 500, 675, 870, 1020]
    #Ed_cb = Ed[list(map(str,cimel_band))]
    #Eds_cb=Eds[list(map(str,cimel_band))]
    #solar_cb=E_solar[list(map(str,cimel_band))]
    Ed_cb = Ed[cimel_band]
    Eds_cb = Eds[cimel_band]
    solar_cb = E_solar[cimel_band]
    
    Ed_cb_i = []
    Eds_cb_i = []
    solar_cb_i = []
    for i in range(len(cimel_band)):
        idxrange = list(range(cimel_band[i]-5,cimel_band[i]+6))
        Ed_cb_i.append(Ed[idxrange].mean(axis=1))
        Eds_cb_i.append(Eds[idxrange].mean(axis=1))
        solar_cb_i.append(E_solar[idxrange].mean(axis=1))
    Ed_cb = pd.concat(Ed_cb_i, axis = 1)
    Eds_cb = pd.concat(Eds_cb_i, axis = 1)
    solar_cb = pd.concat(solar_cb_i, axis = 1)
    Ed_cb.columns = cimel_band
    Eds_cb.columns = cimel_band
    solar_cb.columns = cimel_band
         
    return calc_aot_direct(Ed_cb, Eds_cb, Sza, solar_cb, sed, aod_type)
    

def calc_aod_from_df(data, cimel=False, aod_type=["total_od", "aod_microtops", "aod_wood_2017"], wavelengths=None):
    """coerces data from the format returned from the database to the format for the calculation, and back,
    also loads the reference solar spectrum
    params:
        data: dataframe of all the relevant data, columns = ["pc_time_end_measurement", 
                                                             "global_spectrum", "diffuse_spectrum",
                                                             "sza", "sed"]
        cimel: if True, calculates the aod only at certain wavelengths that cimel instruments measure at
        aod_type: the desired outputs string or list of strings
        wavelengths: filters the wavlengths that are used for the caluclation, and that are returned
    """
    utctime = pd.to_datetime(data["pc_time_end_measurement"]).dt.tz_localize(None)
    
    ed = pd.DataFrame(np.stack(data["global_spectrum"].values), columns = np.arange(300, 1101, 1), index=utctime)
    eds = pd.DataFrame(np.stack(data["diffuse_spectrum"].values), columns = np.arange(300, 1101, 1), index=utctime)
    sza = pd.DataFrame(data["sza"])
    
    if wavelengths is None:
        wavelengths = np.arange(300, 1101, 1)
    else:
        ed = ed[wavelengths]
        eds = eds[wavelengths]
    
    e_solar_df = load_et_spectrum(wavelengths=wavelengths)
    
    aod_data = None
    if cimel:
        aod_data = calc_cimel_band_aot_direct(ed, eds, sza, e_solar_df, data["sed"], aod_type)
    else:
        aod_data = calc_aot_direct(ed, eds, sza, e_solar_df, data["sed"], aod_type)
    
    return aod_data

def load_et_spectrum(filepath=None, wavelengths=None):
    """loads a .txt file containing a reference extraterrestrial solar spectrum, and applies some smoothing
    params:
        filepath: filepath to the file where the spectrum is stored. if None, 
            a default spectrum that comes with the library is used
        wavelengths: which wavelengths to use from the reference file
    returns a dataframe with one row which contains the reference spectrum
    """
    
    if wavelengths is None:
        wavelengths = np.arange(300, 1101)
    
    if filepath is None:
        res = importlib.resources.files("hsr1.data").joinpath("SolarSpectrum.txt")
        file = importlib.resources.as_file(res)
        with file as f:
            filepath = f
    
    e_solar = pd.read_csv(filepath, skiprows=1, delimiter='\t', index_col=0)
    smoothed_e_solar = e_solar.rolling(3).mean().T
    smoothed_e_solar = smoothed_e_solar.fillna(e_solar.T)
    
    e_solar_df = pd.DataFrame(columns=wavelengths)
    e_solar_df.loc[0, :] = smoothed_e_solar[wavelengths].values
    
    return e_solar_df


def calculate_clearsky_wood(data, global_spectrum=None,
                            diffuse_spectrum=None,
                            column="total_od", 
                            absolute_filter:float=2, 
                            relative_filter:float=0.05,
                            relative_time_period:str="10min"):
    """calculates which readings are cloudfree
    
    params:
        data: dataframe with at least columns 
            ["pc_time_end_measurement", "global_spectrum", "diffuse_spectrum", "sza", "sed"]
        column: which aod column to use, one of "total_od", "aod_microtops", "aod_wood_2017"
        absolute_filter: any readings higher than this will be filtered out
        relative_filter: any readings that are more than this value more or less than any
            other within the time window will be filtered out
        relative_time_period: the time period over which the relative filtering is done.
            this is the total time period that the filtering is done by, so if you want
            5 mins either side, pass 10min
            format is a string that will be passed to pd.Timedelta. documentation:
            https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html
    
    returns a numpy array the same length as input dataframe with ones and zeros, 1=clearsky 0=cloud
    """
    aod_data = None
    if global_spectrum is None and diffuse_spectrum is None:
        aod_data = calc_aod_from_df(data, aod_type=column, wavelengths=[500])
    else:
        aod_data = calc_aot_direct(pd.DataFrame(global_spectrum[500]), pd.DataFrame(diffuse_spectrum[500]), pd.DataFrame(data["sza"]), et_wavelengths=[500])
    nm500 = np.stack(aod_data[column].values)[:, 0]
    nm500df = pd.DataFrame(index=pd.DatetimeIndex(data["pc_time_end_measurement"]))
    nm500df["base"] = nm500
    nm500df["max"] = nm500df.rolling(pd.Timedelta(relative_time_period), center=True)["base"].max()-nm500df["base"]
    nm500df["min"] = nm500df.rolling(pd.Timedelta(relative_time_period), center=True)["base"].min()-nm500df["base"]
    nm500df["max"] = np.abs(nm500df["max"])
    nm500df["min"] = np.abs(nm500df["min"])
    nm500df["abs"] = np.logical_and(nm500df["max"] < relative_filter, nm500df["min"] < relative_filter)
    nm500df_abs = np.logical_and(nm500df["max"] < relative_filter, nm500df["min"] < relative_filter)
    
    clearsky_filter = np.logical_and(nm500df_abs.values, nm500 < absolute_filter)
    return clearsky_filter


def calculate_clearsky_filter(data:pd.DataFrame, global_spectrum=None, diffuse_spectrum=None, method:str="wood", kwargs:dict={}):
    """method that calls the appropriate clearsky function
    
    params:
        data: the data that is used for the clearsky calculation
        method: the method that iwll be used to calculate which readings are clearsky readings
        kwargs: the keyword arguments to pass to clearsky_filter
    returns a numpy array the same length as input dataframe with ones and zeros, 1=clearsky 0=cloud
    """
    if method is None:
        return np.ones(len(data)).astype(bool)
    if method == "wood":
        return calculate_clearsky_wood(data, global_spectrum, diffuse_spectrum, **kwargs)
    
    print("filtering method not recognised, not filtering")
    return np.ones(len(data)).astype(bool)




def Get_hsr_Dates(hsr_path, start_date, end_date):
# Get a list of hsr datafiles in the root folder

    folderlist = None
    if hsr_path == "":
        folderlist = os.listdir()
    else:
        folderlist = os.listdir(hsr_path)
    
    datelist = []
    for i, name in enumerate(folderlist):
        try:
            res = bool(dt.datetime.strptime(name[:10], '%Y-%m-%d'))
            datelist.append(name[:10])
        except ValueError:
            res = False
            
    date_dict = dict.fromkeys(datelist, True)     # removes any duplicate dates
    try: 
        # check dates are in range
            for i, name in enumerate(date_dict):
                if len(start_date):
                    if dt.datetime.strptime(name, '%Y-%m-%d') < dt.datetime.strptime(start_date[:10], '%Y-%m-%d'):   
                        date_dict[name] = False
                if len(end_date):
                    if dt.datetime.strptime(name, '%Y-%m-%d') > dt.datetime.strptime(end_date[:10], '%Y-%m-%d'):   
                        date_dict[name] = False
               
    except:
        print('Error checking dates')
        print("start_date: "+str(start_date))
        print("end_date: "+str(end_date))
    
    #print (date_dict)
    hsr_dates  = [k for k, v in date_dict.items() if v == True]
    return hsr_dates



