# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import datetime

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import numpy as np

from hsr1.plots import graphUtils

import time

class LinearTimeGraph:
    def __init__(self, timezone=None, diffuse_name="dif"):
        self.diffuse_name = diffuse_name
        self.timezone = timezone
        ##### according to brsn limits, highest possible global value is 1407
        self.max_integral = 1407
        self.requirements = {"all":["pc_time_end_measurement", "global_integral", "diffuse_integral", "direct_normal_integral"],
                             "ghi":["pc_time_end_measurement", "global_integral"],
                             "diff":["pc_time_end_measurement", "diffuse_integral"],
                             "dni":["pc_time_end_measurement", "direct_normal_integral"]}
        
        self.flags = None
    
    
    def linear_integral_plot_all(self, df, axes, time_col, data_col, show_xlabels=True, date_gap=None, date_gap_scale=1000):
        """plots the intensity per minute (or per several minutes)
        params:
            df: the data to be plotted
            axes: the axes to be plotted on
            time_col: the name of the column containing time data
            data_col: the name of the column containing intensity data
            show_xlabels: whether or not to show the x axes labels. useful when plotting multiple of these graphs with the same labels
            date_gap: the proportion of readings to include, 1/min gets very slow
            date_gap_scale: when no date_gap is specified, this can generate a date gap value based on the size of the dataset
        """
        df = df.copy()
        
        df[time_col] = pd.DatetimeIndex(df[time_col]).tz_localize(None)
        
        if min(df[data_col]) == max(df[data_col]):
            print("min value is the same as max value")
            return
        
        max_height = round(max(df[data_col]))
        max_height = round(self.max_integral)
        
        bbox = axes.get_window_extent()
        horizontal_pixels = int(bbox.width)
        
        
        colordict = {
            "red":((0,1,1), (1,0,0)),
            "green":((0,1,1), (1,0,0)),
            "blue":((0,1,1), (1,1,1))}
        cmap = LinearSegmentedColormap("LinearCmap", colordict)
        
        if date_gap == None:
            date_gap = len(df)//date_gap_scale
            date_gap = max(date_gap, 1)
        
        
        
        measured_timestamps = df["pc_time_end_measurement"]
        first_reading_int = np.datetime64(str(measured_timestamps.iloc[0].date())+" 00:00:00").astype("int64")*10**9
        last_reading_int = np.datetime64(str(measured_timestamps.iloc[len(df)-1].date())+" 23:59:59").astype("int64")*10**9
        measured_timestamps = measured_timestamps.values.astype("int64")
        
        diff = np.diff(measured_timestamps)
        min_diff = np.min(diff[diff>0])
        num_groups = round((last_reading_int-first_reading_int)/min_diff)
        pixels_to_use = min(num_groups, horizontal_pixels)
        
        pixel_timestamps = np.linspace(first_reading_int, last_reading_int, pixels_to_use)
        
        
        readings_df = pd.DataFrame()
        readings_df[time_col] = pd.DatetimeIndex(pixel_timestamps)
        if self.flags is not None:
            df["flags"] = self.flags.any(axis=1)
        
        readings_df = readings_df.merge(df, on=time_col, how="outer").replace(np.nan, 0)
        
        readings_df["int_time"] = readings_df[time_col].astype("int64")
        
        
        def closest_bin(i):
            timestamp = readings_df.loc[i, "int_time"]
            return pixel_timestamps[np.argmin(np.abs(pixel_timestamps-timestamp))]
        
        readings_df = readings_df.groupby(closest_bin).max()
        
        
        data = [np.concatenate((np.zeros(max_height-max(0, round(x))), np.ones(max(0,round(x))))) for x in readings_df[data_col].clip(upper=self.max_integral)]
        data = np.array(data).T
        
        extent = (min(df[time_col]).timestamp(), max(df[time_col]).timestamp(), 0, self.max_integral)
        
        
        axes.imshow(data, aspect="auto", interpolation="none", vmin=0, cmap=cmap, extent=extent)
        
        
        if self.flags is not None:
            colordict = {
                "red":((0,1,1), (1,1,1)),
                "green":((0,1,1), (1,0,0)),
                "blue":((0,1,1), (1,1,1))}
            flag_cmap = LinearSegmentedColormap("LinearCmap", colordict)
            
            any_flags = pd.DataFrame()
            any_flags["flags"] = readings_df["flags"]
            
            flagged = readings_df["flags"].values
            
            flagged_data = data*(flagged.T)
            
            axes.imshow(data, alpha=flagged_data.astype(float), aspect="auto", interpolation="none", vmin=0, cmap=flag_cmap, extent=extent)
        
        
        xticks, labels = graphUtils.calculate_date_labels(df[time_col], axes.get_xlim())
        if not show_xlabels:
            labels = []
        
        axes.set_xticks(xticks, labels)
    
    
    def ghi(self, axes, df, show_xlabels=True, timezone=None):
        """graphs a linear time plot for ghi
        params:
            axes: the axes to plot on
            df: the data to be plotted
            show_xlabels: wether or not to show labels on the x axis, useful when plotting multiple at once
        """
        self.linear_integral_plot_all(df, axes, "pc_time_end_measurement", "global_integral", show_xlabels)
        axes.set_ylabel("GHI(W/m²)")
    
    def diff(self, axes, df, show_xlabels=True, timezone=None):
        """graphs a linear time plot for ghi
        params:
            axes: the axes to plot on
            df: the data to be plotted
            show_xlabels: wether or not to show labels on the x axis, useful when plotting multiple at once
        """
        self.linear_integral_plot_all(df, axes, "pc_time_end_measurement", "diffuse_integral", show_xlabels)
        axes.set_ylabel(self.diffuse_name+"(W/m²)")
    
    def dni(self, axes, df, show_xlabels=True, timezone=None):
        """graphs a linear time plot for ghi
        params:
            axes: the axes to plot on
            df: the data to be plotted
            show_xlabels: wether or not to show labels on the x axis, useful when plotting multiple at once
        """
        dfa = df.copy()
        dfa["direct_normal_integral"] = dfa["direct_normal_integral"].fillna(0)
        self.linear_integral_plot_all(dfa, axes, "pc_time_end_measurement", "direct_normal_integral", show_xlabels)
        axes.set_ylabel("DNI(W/m²)")
        
    
    
    def graph_all(self, axes, df, flags=None):
        """plots all the possible graphs of this type
        params:
            axes: the axes to be plotted on
        """
        self.flags = flags
        
        self.ghi(axes[0], df[self.requirements["ghi"]], False)
        self.diff(axes[1], df[self.requirements["diff"]], False)
        self.dni(axes[2], df[self.requirements["dni"]], True)