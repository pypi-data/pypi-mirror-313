# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import time
import datetime

import pandas as pd
import numpy as np
import matplotlib
import ephem


def calculate_date_labels(time_series:pd.Series, xlims, target_num_ticks:int=10):
    """evenly arranges date labels along the bottom of a daily plot.
    only works with discrete days, not continuous time data
    params: 
        time_series: series conatining all the dates
        xlims: limits of the x axis [smallest, largest]
        num_ticks: number of ticks to be displayed
    """
    time_series = time_series.astype(str)
    times = time_series.str.slice(stop=10).unique()
    times.sort()
    dates = pd.date_range(times[0], times[-1]).strftime("%d-%b")
    # dates = pd.DatetimeIndex(times).strftime("%d-%b")
    
    num_days = len(dates)
    
    ##### locations that are in the middle of a day
    start_of_day = np.arange(xlims[0], xlims[-1], (xlims[-1]-xlims[0])/num_days)
    valid_tick_spots = start_of_day + (((xlims[-1]-xlims[0])/num_days)/2)
    
    
    period = ((num_days-1)//(target_num_ticks))+1
    
    
    ##### finds a consistent period that will result in as close to target_num_ticks as possible
    xtick_indexes = np.arange(0, num_days, period).astype(int)
        
    xticks = [valid_tick_spots[i] for i in xtick_indexes]
    labels = [dates[i] for i in xtick_indexes]
    
    return xticks, labels


def cbar(axes, fig, max_integral:int, tick_period=100, aspect=25):
    """plots a colorbar and generates labels for it
    params:
        axes: axes or list of axes that the colorbar will steal space from
        fig: figure all the graphs are plotted on
        max_integral: the top of the colorbar
        tick_period: distance between the ticks
        aspect: aspect ratio, 1=square
    """
    cbar = fig.colorbar(matplotlib.cm.ScalarMappable(cmap="jet"), ax=axes, aspect=25, pad=0.01)
    
    yticks = np.arange(0, max_integral+1, tick_period)
    ytick_location = yticks/max_integral
    ytick_location[ytick_location == np.inf] = 0
    cbar.ax.set_yticks(ytick_location, yticks.astype(int))


def calculate_sunrise_sunset(data:pd.DataFrame, timezone:pd.Timedelta):
    """
    params:
        data: dataframe with timestamps and locations in
        timezone: timezone of the data, pd.Timedelta
    returns:
        sunrise_set_df: dataframe containing times of the sunrise and sunset
    """
    df = data.copy()
    df = df.dropna()
    
    df["pc_time_end_measurement"] = pd.DatetimeIndex(df["pc_time_end_measurement"].dt.tz_convert(None))
    
    dates = df["pc_time_end_measurement"].dt.date.unique()
    
    ##### set middle of data, rather than the start
    new_df = pd.DataFrame(index=pd.DatetimeIndex(dates) + pd.Timedelta(12, "hours"))
    
    df = df.sort_values("pc_time_end_measurement")
    new_df = new_df.sort_index()
    
    new_df = pd.merge_asof(new_df, df, left_index=True, right_on="pc_time_end_measurement", direction="nearest")
    new_df[["gps_longitude", "gps_latitude", "gps_altitude"]] = new_df[["gps_longitude", "gps_latitude", "gps_altitude"]].astype(float)
    new_df = new_df.ffill()
    
    
    geopoint = new_df[["gps_longitude", "gps_latitude", "gps_altitude"]].values
    timestamp = pd.to_datetime(new_df.index)
    
    
    sunrise_set_df = pd.DataFrame(index=timestamp)
    
    sun = ephem.Sun()
    
    sunrises = []
    sunsets = []
    for i in range(len(timestamp)):
        instrument = ephem.Observer()
        instrument.date = timestamp[i]
        instrument.lat = str(geopoint[i][1])
        instrument.lon = str(geopoint[i][0])
        instrument.elevation = geopoint[i][2]
        
        try:
            sunrise = instrument.next_rising(sun)
            sunrises.append(sunrise.datetime())
        except ephem.AlwaysUpError:
            sunrises.append(None)
        except ephem.NeverUpError:
            sunrises.append(None)
        
        try:
            sunset = instrument.next_setting(sun)
            sunsets.append(sunset.datetime())
        except ephem.AlwaysUpError:
            sunsets.append(None)
        except ephem.NeverUpError:
            sunsets.append(None)
    
    ##### convert back to local time
    sunrise_set_df["sunrise"] = np.array(sunrises)+timezone
    sunrise_set_df["sunset"] = np.array(sunsets)+timezone
    
    return sunrise_set_df


    
def plot_reference_lines_and_labels(axes, left_edge=0, reference_lines=None, reference_labels=None):
    if reference_lines is None:
        reference_lines = [374, 384, 393, 430, 487, 517, 590, 657, 688, 719, 761, 817, 900, 936, 976]
    if reference_labels is None:
        reference_labels = ["Fe", "Ca+", "Ca+", "Ca/Fe", "H-B", "Mg", "Na", "H-A", "O2", "H2O", "O2", "O2", "", "", ""]
    elif reference_labels == []:
        reference_labels = [""]*len(reference_lines)
    
    
    fancy_strings = []
    ##### add dashes if not epmpty string
    for j in range(len(reference_labels)):
        reference_labels[j] = reference_labels[j] +" - " if reference_labels[j] != "" else ""
        fancy_strings.append(reference_labels[j]+str(reference_lines[j]))
    
    ##### plus 0.5 so lines are in the middle of the pixel, not the bottom
    reference_lines = np.array(reference_lines)+0.5
    for i in range(len(reference_lines)):
        axes.axhline(y=reference_lines[i], color="black", linewidth=0.4)
        axes.axhline(y=reference_lines[i], color="lightgray", linewidth=0.3)

    axes.set_yticks(reference_lines, fancy_strings)
    axes.tick_params(axis='y', which='major', labelsize=10)

def superscript(number):
    if type(number) != int:
        raise TypeError("number to be superscripted must be an int")
    superscript_chars = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    result = ""
    if number < 0:
        result = "⁻"
        number = abs(number)
    for num in str(number):
        result += superscript_chars[int(num)]
    
    return result



def generate_metadata_string(deployment_metadata, data=None):
    #### make a dict of name: value pairs
    metadata = {}
    
    metadata["lat"] = deployment_metadata['default_latitude'][0]
    metadata["lon"] = deployment_metadata['default_longitude'][0]
    
    if data is not None:
        metadata["period"] = str(data.iloc[0]["pc_time_end_measurement"].date()) + " - " + str(data.iloc[len(data)-1]["pc_time_end_measurement"].date())
        metadata["total readings"] = str(len(data))
    
    ##### convert dict to string
    output = ""
    for line in metadata.keys():
        if metadata[line] != "''":
            output += line+": "+metadata[line]+", "
    
    ##### crop trailing ", "
    return output[:-2] + "\n"

def total_seconds(timestamp):
    return (timestamp - datetime.datetime(1970, 1, 1, )).total_seconds()

def make_full_title(title):
    return title.replace("<", "_").replace(">", "_").replace(":", "_").replace("/", "_").replace("\\", "_").replace("|", "_").replace("?", "_").replace("*", "_").replace("\"", "_").replace("\n", " ").replace("\"", "'").replace("|", "_")


def numpy_string_slice(a, start, end):
    b = a.view((str,1)).reshape(len(a),-1)[:,start:end]
    return np.fromstring(b.tostring(),dtype=(str,end-start))
