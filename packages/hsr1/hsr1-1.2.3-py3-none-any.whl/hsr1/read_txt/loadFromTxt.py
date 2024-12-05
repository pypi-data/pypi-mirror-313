# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import pandas as pd
import os
import zipfile

import numpy as np

import hsr1.read_txt.ImportHSRFiles as ImportHSRFiles
from hsr1.utils import (HSRFunc as hsr_func,
                       reformatData)

from hsr1 import DBDriver




def read(hsr_path="", start_date="2000-01-01", end_date="2100-01-01", deployment_metadata_filepath=None):
    """reads all the commonly used data from the .txt files. only loads the global and diffuse spectrum
    params:
        hsr_path: the filepath to the data that will be read. 
            this folder should contain one .zip file for each day, named YYYY-MM-DD.zip
        start_date: the first date that is read from the folder of zip files, inclusive.
            should be in the format YYYY-MM-DD
        start_date: the last date that is read from the folder of zip files, inclusive.
            should be in the format YYYY-MM-DD
        deployment_metadata_filepath: the filepath to the deployment metadata .ini file that will be read
    
    returns:
        tuple of dataframes that can be stored to the database using DBDriver.store()
            one dataframe per table in the database
    """
    
    if deployment_metadata_filepath is None:
        raise ValueError("a deployment_metadata_filepath must be passed")
    
    hsr_dates  = hsr_func.Get_hsr_Dates(hsr_path, start_date, end_date)
    if len(hsr_dates) == 0:
        raise ValueError(f"No data could be found for the supplied dates: {start_date}, {end_date}")
    
    gps_type = "gps"
    gps_file_name = "GPS.txt"
    
    filename = os.path.join(hsr_path, hsr_dates[0] + '.zip')
    if os.path.isfile(filename):    # for data in zipfiles
        day_one = zipfile.ZipFile(filename)
        if "AccessoryData.txt" in day_one.namelist():
            gps_type = "accessory"
            gps_file_name = "AccessoryData.txt"
    elif os.path.isdir(os.path.join(hsr_path, hsr_dates[0])):     # for data expanded into dated folders
        if os.path.isfile(os.path.join(hsr_path, hsr_dates[0] + "/AccessoryData.txt")):
            gps_type = "accessory"
            gps_file_name = "AccessoryData.txt"
    
    m_Ed = []
    m_Eds = []
    m_Summary = []
    m_Gps = []
    m_IndCh = []
    
    
    for hsr_date in hsr_dates:
        print("reading "+hsr_date)
        dfTemp = ImportHSRFiles.open_hsr_file(hsr_path, hsr_date, 'Total.txt')
        if len(dfTemp): 
            m_Ed.append( dfTemp)
        dfTemp =  ImportHSRFiles.open_hsr_file(hsr_path, hsr_date, 'Diffuse.txt')
        if len(dfTemp): 
            m_Eds.append(dfTemp)
        dfTemp = ImportHSRFiles.open_hsr_file(hsr_path, hsr_date, 'Summary.txt')
        if len(dfTemp): 
            m_Summary.append(dfTemp)
        dfTemp = ImportHSRFiles.open_hsr_file(hsr_path, hsr_date, 'IndCh.txt')
        if len(dfTemp):
            m_IndCh.append(dfTemp)
        dfTemp = ImportHSRFiles.open_hsr_file(hsr_path, hsr_date, gps_file_name)
        if len(dfTemp):
            m_Gps.append(dfTemp)
    
    
    if len(m_Ed): 
        ed = pd.concat(m_Ed)
    else: ed = None
    if len(m_Eds):
        eds = pd.concat(m_Eds)
    else: eds = None
    if len(m_Summary): 
        summary = pd.concat(m_Summary)  
    else: summary = None
    if len(m_IndCh): 
        ind_ch = pd.concat(m_IndCh)
    else: ind_ch = None
    if len(m_Gps):
        gps = pd.concat(m_Gps)
    else: gps = None
        
    reformatter = reformatData.ReformatData()
    
    reformatted = reformatter.reformat_data([ed, eds, summary, ind_ch, gps], deployment_metadata_filepath, gps_type)
    
    return reformatted
    


def read_raw_txt(hsr_path="", start_date="2000-01-01", end_date="2100-01-01", deployment_metadata_filepath=None):
    """reads each channel of spectral data from the .txt files
    params:
        hsr_path: the filepath to the data that will be read. 
            this folder should contain one .zip file for each day, named YYYY-MM-DD.zip
        start_date: the first date that is read from the folder of zip files, inclusive.
            should be in the format YYYY-MM-DD
        start_date: the last date that is read from the folder of zip files, inclusive.
            should be in the format YYYY-MM-DD
        deployment_metadata_filepath: the filepath to the deployment metadata .ini file that will be read
    
    returns a tuple of dataframes that can be used with DBDriver.store_raw to make a raw dataset
    """
    if deployment_metadata_filepath is None:
        raise ValueError("a deployment_metadata_filepath must be passed")
    
    hsr_dates  = hsr_func.Get_hsr_Dates(hsr_path, start_date, end_date)
    if len(hsr_dates) == 0:
        print("warning, no dates selected to read")
    
    filenames = []
    for hsr_date in hsr_dates:
        filename = os.path.join(hsr_path, hsr_date + '.zip')
        if os.path.isfile(filename):    # for data in zipfiles
            zip_obj = zipfile.ZipFile(filename)
            for name in zip_obj.namelist():
                if "Raw" in name and name not in filenames:
                    filenames.append(name)
        elif os.path.isdir(os.path.join(hsr_path, hsr_date)):     # for data expanded into dated folders
            for name in os.listdir(os.path.join(hsr_path, hsr_date)):
                if "Raw" in name and name not in filenames:
                    filenames.append(name)

            
    dfs = [[] for i in range(len(filenames))]
    
    for hsr_date in hsr_dates:
        print("reading "+hsr_date)
        
        for i, filename in enumerate(filenames):
            df_temp = ImportHSRFiles.open_hsr_file(hsr_path, hsr_date, filename, Raw=True)
            if len(df_temp): 
                dfs[i].append(df_temp)
    
    for i, df in enumerate(dfs):
        dfs[i] = pd.concat(df)
    
    reformatter = reformatData.ReformatData()
    deployment_metadata = reformatter.reformat_deployment_metadata(deployment_metadata_filepath)
    
    return dfs, deployment_metadata


def read_raw_pixels(file_path=None, skiprows=2):
    """reads the raw pixel data for each channel in the .txt files
    params:
        file_path: the filepath to the data that will be read. 
            this folder should contain one .zip file for each day, named YYYY-MM-DD.zip
        skiprows: the nuber of rows at the top of each file to skip when reading
    """
    single = False
    files = None
    if file_path is None:
        files = os.listdir()
    else:
        if os.path.isdir(file_path):
            files = os.listdir(file_path)
        else:
            files = [file_path]
            single = True
    
    all_columns = []
    
    dictlist = []
    for file_name in files:
        file = file_name
        if not single:
            file = file_path + "/" + file_name
        temp_df = pd.read_csv(file, sep="\t", skiprows=skiprows)
        tempdict = {}
        tempdict["pc_time_end_measurement"] = None
        file_columns = list(temp_df.columns)
        
        del file_columns[0]
        
        for col in file_columns:
            if not col in all_columns:
                all_columns.append(col)
        
        for column in file_columns:
            tempdict[column] = temp_df[column].to_numpy()[:-1]
        dictlist.append(tempdict)
    
    df_columns = []
    for file_col in all_columns:
        df_columns.append(file_col.replace("Ch", "channel_"))
    
    
    result = pd.DataFrame(dictlist)
    result.columns=["pc_time_end_measurement"]+df_columns
    return result


def store_segmented(db_driver, hsr_path, start_date, end_date, period=1, precalculated_values=True, temp_databases_location="temp_databases/"):
    """stores a dataset from txt in seperate databases, and merges them"""
    store_seperate(hsr_path, start_date, end_date, period, precalculated_values, temp_databases_location, _raise=True)
    db_driver.db_store.combine_database_folder(temp_databases_location, delete=True)

def store_seperate(hsr_path, start_date, end_date, deployment_metadata_file_path, period=1, precalculated_values=True, temp_databases_location="temp_databases/", db_type="sqlite", _raise=False):
    """stores a dataset into multiple databases"""
    hsr_dates = hsr_func.Get_hsr_Dates(hsr_path, start_date, end_date)
    
    if not os.path.isdir(temp_databases_location):
        os.mkdir(temp_databases_location)
    
    prev_files = os.listdir(temp_databases_location)
    if len(prev_files) > 0:
        if _raise:
            raise FileExistsError("there are already files in the target directory")
        print("WARNING: there are already files in the target directory")
        
    
    list_of_lists = []
    for i in range(0, len(hsr_dates)-period, period):
        list_of_lists.append(hsr_dates[i:i+period])
    list_of_lists.append(hsr_dates[i+period:])
    
    reformatter = reformatData.ReformatData()
    
    for small_hsr_dates in list_of_lists:
        db_name = "temp_db_"+small_hsr_dates[0]+".db"
        db_type = db_type

        temp_driver = DBDriver(temp_databases_location+db_name, db_type, deployment_metadata_file_path)
        
        dfs, gps_type = read(hsr_path, small_hsr_dates[0], small_hsr_dates[-1])
        reformatted = reformatter.reformat_data(dfs, deployment_metadata_file_path, gps_type)
        temp_driver.db_store.store(reformatted, temp_driver)
        if precalculated_values:
            temp_driver.add_precalculated_values()





def store_to_hdf(file_path, ed, eds, summary, hdr, ind_ch, gps):
    ##### makes the folder file_path if it dosent exist
    if not os.path.isdir(file_path):
        print("hdfs folder dosent exist, making a new one")
        strings = file_path.split("/")
        string_path = ""
        for string in strings[:-1]:
            string_path += string+"/"
            if not os.path.isdir(string_path):
                os.mkdir(string_path)
    
    ##### stores dataframes to hdf
    ed.to_hdf(file_path+"ed", "ed")
    eds.to_hdf(file_path+"eds", "eds")
    summary.to_hdf(file_path+"summary", "summary")
    hdr.to_hdf(file_path+"hdr", "hdr")
    ind_ch.to_hdf(file_path+"indch", "indch")
    gps.to_hdf(file_path+"gps", "gps")


def load_from_hdf(file_path):
    ed = pd.read_hdf(file_path+"ed", "ed")
    eds = pd.read_hdf(file_path+"eds", "eds")
    summary = pd.read_hdf(file_path+"summary", "summary")
    hdr = pd.read_hdf(file_path+"hdr", "hdr")
    ind_ch = pd.read_hdf(file_path+"indch", "indch")
    gps = pd.read_hdf(file_path+"gps", "gps")
    
    return [ed, eds, summary, hdr, ind_ch, gps]