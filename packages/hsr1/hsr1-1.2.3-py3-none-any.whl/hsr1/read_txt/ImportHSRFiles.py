# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import warnings
import datetime
import os, io
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import matplotlib.dates as mdates
import datetime as dt
import zipfile 

import ephem

##### supressing pandas performance warnings
warnings.simplefilter(action='ignore', category=pd.errors.DtypeWarning)

def calc_sun_zenith_azimuth(ts, lat, lon):
    obs = ephem.Observer()
    sun = ephem.Sun()

    obs.date = ts
    obs.lat, obs.lon = str(lat), str(lon)

    sun.compute(obs)

    return 90 - (sun.alt * 180. / np.pi)#, sun.az * 180. / np.pi

def open_gps_file(hsr_path, hsr_date):
    # hsr_path is root folder for the dataset, hsr date is text representation of the date
    filename = os.path.join(hsr_path, hsr_date, '.zip')
    GPS = []
    if os.path.isfile(filename):
        try:    # try the quick read, works for uninterrupted files
            archive = zipfile.ZipFile(filename, 'r')
            ### Import hsr GPS from daily folder
            #GPS = pd.read_csv(archive.open( 'GPS.txt'), skiprows=1, delimiter='\t', parse_dates=['PC Time','GPS Time'], index_col=0, converters = {'Status': str})
            with archive.open('GPS.txt') as datafile:
                GPS = read_by_line(datafile, hsr_date)
            
        except:     # try a line-by-line read
            print ("Error reading zip, trying line-by-line " + filename)

    elif os.path.isdir(os.path.join(hsr_path, hsr_date)):
        filename = os.path.join(hsr_path, hsr_date, 'GPS.txt')
        try:    # try the quick read, works for uninterrupted files
        
            #GPS = pd.read_csv(filename, skiprows=1, delimiter='\t', parse_dates=['PC Time','GPS Time'], index_col=0, converters = {'Status': str})
            with open(filename) as datafile:
                GPS = read_by_line(datafile, hsr_date)
        except:     # try a line-by-line read
            print ("Error reading, trying line-by-line  " + filename)
    
    return GPS

def read_by_line(datafile, hsr_date):
    # print('read-by-line ' + hsr_date + ' ' + os.path.basename(datafile.name))
    row_list=[]        # list which stores date time row objects
    dt_list = []        # list which stores the actual date-times
    element_list=[] # list which stores the elements of each row
    column_list = np.arange(300,1101)    # list which stores the column headings, default is for Raw files
    for i, row in enumerate(datafile):
        dict1 = {}
        if row[:10] == hsr_date: # tests for line which contains radiance entries (first 10 elements are date)
            date_time_string=row[0:19]
            if not date_time_string:  # break condition for empty string
                break
            element_list = row.strip().split("\t")[1:]      # strip gets rid of line ends in last item
            if len(column_list) <= len(element_list):
                for count, value in enumerate(column_list):
                    try:
                        # dict1.update({value:float(element_list[count])}) ##### <- previous line, access by key is a bit faster
                        dict1[value] = float(element_list[count])    # convert to a number if it will
                    except ValueError:
                        dict1[value] = element_list[count]       # otherwise treat as a string
                row_list.append(dict1)
                dt_list.append(dt.datetime.strptime(date_time_string,'%Y-%m-%d %H:%M:%S'))
        elif  'Time' in row[:10]:
            column_list = row.strip().split("\t")[1:]
    # now turn it into a dataframe
    df = pd.DataFrame(row_list)
    if len(row_list) == 0:
        return pd.DataFrame()
    df.columns=column_list
    df.index = dt_list
    return  df 
    
def open_hsr_file(hsr_path, hsr_date, hsr_file, Raw=False):
    # hsr_path is root folder for the dataset, hsr_date is text representation of the date
    filename = os.path.join(hsr_path, hsr_date + '.zip')
    if hsr_file == 'GPS.txt':
        time_cols = ['PC Time', 'GPS time']
    else:
        time_cols = ['Time']
        
    hsr_df = []
    if os.path.isfile(filename):    # for data in zipfiles
        try:    # try the quick read, works for uninterrupted files
            archive = zipfile.ZipFile(filename, 'r')
            ### Import hsr file from daily folder
            if Raw==True:
                hsr_df = pd.read_csv(archive.open( hsr_file), skiprows=1, delimiter='\t', index_col=0, header=None)                
                hsr_df.columns = np.arange(300, 1101)
            else:
                hsr_df = pd.read_csv(archive.open( hsr_file), skiprows=2, delimiter='\t',parse_dates=time_cols,  index_col=0)
            hsr_df.index = pd.to_datetime(hsr_df.index)
        except KeyError:
            return hsr_df
        except:     # try a line-by-line read
            # print ("Error reading zip, trying line-by-line " + filename)
            with io.TextIOWrapper(archive.open(hsr_file), encoding="utf-8") as datafile:
                hsr_df = read_by_line(datafile, hsr_date)

    elif os.path.isdir(os.path.join(hsr_path, hsr_date)):     # for data expanded into dated folders
        filename = os.path.join(hsr_path, hsr_date, hsr_file)
        try:    # try the quick read, works for uninterrupted files
            if Raw==True:
                hsr_df = pd.read_csv(filename, skiprows=1, delimiter='\t', index_col=0, header=None)                
                hsr_df.columns = np.arange(300, 1101)
            else:        
                hsr_df = pd.read_csv(filename, skiprows=2, delimiter='\t', parse_dates=time_cols, index_col=0)
            hsr_df.index = pd.to_datetime(hsr_df.index)
        except KeyError:
            return hsr_df
        except:     # try a line-by-line read
            # print ("Error reading, trying line-by-line  " + filename)
            try: 
                with open(filename) as datafile:
                    hsr_df = read_by_line(datafile, hsr_date)
            except:
                return []
    
    return hsr_df[hsr_df.index.notnull()]

def load_Raw_series(hsr_dates, hsr_path, Series_filename, Compress = False):
    # hsr_dates is a list of dates to load
    # hsr_path is the root of the datastructure
    # Series_filename is the name of the HDF filename to save the data to, in hsr_path
    #load up raw values - do a day at a time
    m_Raw = []
    Raw = []
    for i in range(0,8):
        m_Raw.append([])
        Raw.append([])
    for hsr_date in hsr_dates:
        for i in range(0,8):
            filename = 'Raw {}.txt'.format(i)
            fRaw = open_hsr_file(hsr_path, hsr_date, filename, True)
            if len(fRaw):
                if Compress == True:    #reduce to 1-min averages
                    fRaw = fRaw.astype(float).resample('1T',label = 'right', closed = 'right').mean().dropna(how='all')
                m_Raw[i].append(fRaw)
        print("loaded Raw files for " + hsr_date)
    for i in range(0,8):
        Raw[i] = pd.concat(m_Raw[i])
        keyname = 'Raw{}'.format(i)
        Raw[i].to_hdf(Series_filename, key = keyname)
    return Raw

def time_WL_plot(spectra_1,spectra_2,name_1,name_2,timestamp,wl_range): # function for 2D colorplots
    # inputs: spectra_1 and spectra_2 are 2D np.arrays (rows==timestamp, columns==wavelength),
    # name 1 and 2 are corresponding variable names, and timestamp is a datetimelist
    
    datestamp=timestamp[0].date() # date
    spec_D=(spectra_1-spectra_2).T   # tranposed spectral difference
    
    pl.figure(figsize=(18,14))

    #  timestamp plot limits - 6 and 16 UTC are default
    llim=mdates.date2num(dt.datetime(datestamp.year,datestamp.month,datestamp.day,4,0,0))  
    ulim=mdates.date2num(dt.datetime(datestamp.year,datestamp.month,datestamp.day,20,0,0))
    
    time_day_ar = np.array(timestamp) # convert to np array format
    wl_ar = np.array(wl_range)
    
    pl.title(name_1 +' - ' + name_2 + ':  {}'.format(datestamp.strftime('%Y-%m-%d')),size=18)
    pl.pcolormesh(time_day_ar,wl_ar,spec_D,cmap='bwr')
    #pl.pcolormesh(time_day_ar,wl_range,spec_D,cmap='bwr') $ no limits
    pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    pl.gca().yaxis.set_major_locator(pl.MultipleLocator(100) )
    pl.tight_layout()
    pl.gca().invert_yaxis()
    pl.ylabel("Wavelength [nm]")
    pl.xlabel("UTC time [hrs]")
    pl.xlim(llim,ulim)
    #pl.ylim(350,900)
    #pl.yaxis.set_major_locator(ticker.AutoLocator())
    cbar=pl.colorbar(orientation="horizontal")
    cbar.set_label(name_1 +' - ' + name_2 + ' [$mW m^{-2} nm^{-1}]$',size=18)



def time_WL_plot2(dfSpectrum, title): # function for 2D colorplots
    # inputs: dfSpectrum is a Pandas dataframe containing time v spectral data
    # title is some text to go in the title
    
    wl_range=dfSpectrum.columns
    timestamp = dfSpectrum.index   

    datestamp=timestamp[0].date() # date
    spec_D=dfSpectrum.T   # tranposed spectrum
    
    pl.figure(figsize=(18,14))

    #  timestamp plot limits - 6 and 16 UTC are default
    llim=mdates.date2num(dt.datetime(datestamp.year,datestamp.month,datestamp.day,15,0,0))  
    ulim=mdates.date2num(dt.datetime(datestamp.year,datestamp.month,datestamp.day,17,0,0))
    
    time_day_ar = np.array(timestamp) # convert to np array format
    wl_ar = np.array(wl_range)
    
    pl.title(title + ':  {}'.format(datestamp.strftime('%Y-%m-%d')),size=18)
    pl.pcolormesh(time_day_ar,wl_ar,spec_D,cmap='bwr')
    #pl.pcolormesh(time_day_ar,wl_range,spec_D,cmap='bwr') $ no limits
    pl.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    pl.gca().yaxis.set_major_locator(pl.MultipleLocator(100) )
    pl.tight_layout()
    pl.gca().invert_yaxis()
    pl.ylabel("Wavelength [nm]")
    pl.xlabel("UTC time [hrs]")
    pl.xlim(llim,ulim)
    #pl.ylim(350,900)
    #pl.yaxis.set_major_locator(ticker.AutoLocator())
    cbar=pl.colorbar(orientation="horizontal")
    cbar.set_label('Intensity' + ' [$mW m^{-2} nm^{-1}]$',size=18)





if __name__ == '__main__':
    
    """    
     hsr_path='D:\DOCUMENT\BF4 Spectral\SolarSpectrumLogging\HSR1-003\Danube 2021' # path to directory containing all the hsr .txt files
     hsr_date='2021-10-11'    # clean files
     
    # clean = open_gps_file(hsr_path, hsr_date)
     total = open_hsr_file(hsr_path, hsr_date, 'Total.txt')
     diffuse = open_hsr_file(hsr_path, hsr_date, 'Diffuse.txt')
     summary = open_hsr_file(hsr_path, hsr_date, 'Summary.txt')
    # gps = open_hsr_file(hsr_path, hsr_date, 'GPS.txt')
     hsr_date='2020-10-29'    # broken files
    # broken = open_gps_file(hsr_path, hsr_date)
    """

    # hsr_path='D:\DOCUMENT\BF4 Spectral\SolarSpectrumLogging\HSR1-002\PMLQuest 2021' # path to directory containing all the hsr .txt files
    # hsr_date='2021-08-03'    # 
    # lat = 50.37
    # lon = -4.13
    # Ed = open_hsr_file(hsr_path, hsr_date, 'Total.txt')
    # #Eds = open_hsr_file(hsr_path, hsr_date, 'Diffuse.txt')
    # Summary = open_hsr_file(hsr_path, hsr_date, 'Summary.txt')
    
    # time_WL_plot2(Ed, 'Ed only')
    """
    hsr_path='D:\DOCUMENT\BF4 Spectral\SolarSpectrumLogging\HSR1-001\Winster 2021' # path to directory containing all the hsr .txt files
    hsr_date='2021-09-21'
    filename = 'Total.txt'
    Ed = open_hsr_file(hsr_path, hsr_date, 'Total.txt')
    Eds = open_hsr_file(hsr_path, hsr_date, 'Diffuse.txt')
    wl_range=Ed.columns
    timestamp = Ed.index   
    time_WL_plot(Ed, Eds, 'Ed', 'Eds',timestamp, wl_range )
    time_WL_plot2(Ed, 'Ed only')
    """



