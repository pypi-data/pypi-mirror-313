# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from hsr1.plots import graphUtils

import time

class TimeDayGraph:
    def __init__(self, cmap=plt.get_cmap("jet"), timedelta=pd.Timedelta(0), diffuse_name="dif"):
        self.diffuse_name = diffuse_name
        self.cmap = cmap
        ##### according to brsn limits, highest possible global value is 1407
        self.max_integral = None
        self.requirements = {"all":["pc_time_end_measurement", "global_integral", "diffuse_integral", "direct_normal_integral", "gps_longitude", "gps_latitude", "gps_altitude"],
                             "ghi":["pc_time_end_measurement", "global_integral", "gps_longitude", "gps_latitude", "gps_altitude"],
                             "diff":["pc_time_end_measurement", "diffuse_integral", "gps_longitude", "gps_latitude", "gps_altitude"],
                             "dni":["pc_time_end_measurement", "direct_normal_integral", "gps_longitude", "gps_latitude", "gps_altitude"]}
        self.flags = None
        self.timedelta = timedelta
        
    
    def time_day_graph(self, 
                       df:pd.DataFrame, 
                       axes, 
                       time_col:str, 
                       data_col:str, 
                       sunrise_sunset=None, 
                       show_xlabels:bool=True, 
                       show_cbar=True,
                       stack_resolution="max"):
        """plots one column of data onto a plot with minutes in a day in one axes and days on another
        params:
            df: data to be plotted
            axes: axes on which data will be plotted
            time_col: name of column in data that contains the time of each datapoint
            data_col: name of column in data that contains the data to be plotted
            sunrise_sunset: the sunrise and sunset data. if None, not plotted
            show_xlabels: whether or not to show the x axes labels. useful when plotting multiple of these graphs with the same labels
            show_cbar: whether or not to show the colorbar. useful when plotting multiple of these graphs with the same colormap
            stack_resolution: ("max"/"mean"/"min") when there are more readings
                than pixels, how to resolve the multiple readings that correspond
                to each pixel.
        """
        df = df.copy()
        
        if self.max_integral is None:
            self.max_integral = np.nanmax(df[data_col])
        
            
        bbox = axes.get_window_extent()
        vert_pixels = int(bbox.height)
        
        datetimeindex = pd.DatetimeIndex(df[time_col]).tz_localize(None)
        
        start = df.loc[0, time_col].tz_localize(None)
        stop = df.loc[len(df)-1, time_col].tz_localize(None)
        dates = pd.date_range(start, stop, normalize=True).date
        
        ##### generates the new index seperated by days and minutes
        new_index = [datetimeindex.date, datetimeindex.hour*60+datetimeindex.minute+datetimeindex.second/60]
        
        ##### sets the new index and unstacks it, which converts the dataframe from having 2 indexes,
        #####   to having 1 index, and for each column, having n columns, where n is the number of days
        new_df = df.set_index(new_index).unstack(level=0)
        
        ##### convert to hours, more human readable
        new_df.index = new_df.index/60
        
        new_df = new_df[data_col]
        new_df = new_df.reindex(columns=dates)
        
        extent = (pd.to_datetime(dates[0]).timestamp(), pd.to_datetime(dates[-1]+pd.Timedelta(1, "day")).timestamp(), 24, 0)
        
        ##### find the smallest number of groups that can represent all 
        #####   the data loslessly. if impossible use the max number of groups
        #####   that will fit onto the graph
        diff = np.diff(new_df.index)
        min_diff = np.min(diff[diff>0])
        
        ##### convert to hours
        num_groups = round(24/min_diff)
        pixels_to_use = min(num_groups, vert_pixels)

        pixel_hours = np.linspace(0, 24, pixels_to_use, endpoint=False)
        measured_hours = np.array(new_df.index)
        
        # ##### finds the closest pixel to each reading's true value
        def closest_pixel_hour(i):
            return pixel_hours[np.argmin(np.abs(pixel_hours-i))]
        
        ##### groups all the readings into one pixel groups, according to the
        #####   stack_resolution parameter
        if stack_resolution == "max":
            new_df = new_df.groupby(closest_pixel_hour).max()
        elif stack_resolution == "mean":
            new_df = new_df.groupby(closest_pixel_hour).mean()
        elif stack_resolution == "min":
            new_df = new_df.groupby(closest_pixel_hour).min()
        
        ##### fill the df with nan where there are no readings
        all_pixel_hours = pd.DataFrame(index=pixel_hours)
        new_df = pd.merge(new_df, all_pixel_hours, how="outer", left_index=True, right_index=True)
        
        image = axes.imshow(new_df, aspect="auto", cmap=self.cmap, interpolation="none", extent=extent, vmin=0, vmax=self.max_integral)
        axes.set_ylim(24, 0)
        
        xlim = axes.get_xlim()
        
        
        ##### plots the sunrise and sunset lines
        if sunrise_sunset is not None:
            sunrise_set_date = np.linspace(xlim[0], xlim[1], len(sunrise_sunset))
            
            sunrise_time = sunrise_sunset["sunrise"].dt.hour + sunrise_sunset["sunrise"].dt.minute/60
            sunset_time = sunrise_sunset["sunset"].dt.hour + sunrise_sunset["sunset"].dt.minute/60
            
            if len(sunrise_set_date) == 1:
                sunrise_set_date = np.array([sunrise_set_date[0], sunrise_set_date[0] + 1])
                sunrise_time = np.array([sunrise_time]*2)
                sunset_time = np.array([sunset_time]*2)
            
            axes.plot(sunrise_set_date, sunrise_time, "--", color="white", linewidth=0.5)
            axes.plot(sunrise_set_date, sunset_time, "--", color="white", linewidth=0.5)
        
        
        ##### superimposes the passed flagged data onto the plot
        if self.flags is not None:
            colordict = {
                "red":((0,1,1), (1,1,1)),
                "green":((0,1,1), (1,0,0)),
                "blue":((0,1,1), (1,1,1))}
            flag_cmap = LinearSegmentedColormap("LinearCmap", colordict)
            
            ##### same process as the data graph but with the flagged data
            any_flags = pd.DataFrame()
            any_flags["flags"] = self.flags.any(axis=1)
            new_flag_df = any_flags.set_index(new_index).unstack(level=0)
            new_flag_df = new_flag_df["flags"]
            new_flag_df.index = new_flag_df.index/60
            new_flag_df = new_flag_df.reindex(columns=dates).astype(float)
            
            new_flag_df = new_flag_df.fillna(0)
            
            image = axes.imshow(new_flag_df, aspect="auto", norm=matplotlib.colors.LogNorm(vmin=0, vmax=1), cmap=flag_cmap, interpolation="none", extent=extent)
            
        
        xticks, labels = graphUtils.calculate_date_labels(df[time_col], axes.get_xlim())
        
        if not show_xlabels:
            labels = []
        
        axes.set_xticks(xticks, labels)
        axes.set_yticks(np.arange(0, 25, 6))
        
        if show_cbar:
            self.fig.colorbar(image, ax=axes, pad=0)
    
    
    def ghi(self, axes, df, sunrise_sunset=None, 
            show_xlabels:bool=True, show_cbar:bool=True):
        """graphs a time/day plot for ghi
        params:
            axes: the axes to plot on
            df: the data to be plotted
            sunrise_sunset: times of sunrise and sunset for every day
            show_xlabels: wether or not to show labels on the x axis, useful when plotting multiple at once
            show_cbar: wether or not to show a colorbar, useful when plotting multiple at once
        """
        self.time_day_graph(df, axes, "pc_time_end_measurement", "global_integral", 
                            sunrise_sunset=sunrise_sunset, 
                            show_xlabels=show_xlabels, show_cbar=show_cbar)
        axes.set_ylabel("GHI(W/m²)")
    
    def diff(self, axes, df, sunrise_sunset=None, 
             show_xlabels:bool=True, show_cbar:bool=True):
        """graphs a time/day plot for diffuse
        params:
            axes: the axes to plot on
            df: the data to be plotted
            sunrise_sunset: times of sunrise and sunset for every day
            show_xlabels: wether or not to show labels on the x axis, useful when plotting multiple at once
            show_cbar: wether or not to show a colorbar, useful when plotting multiple at once
        """
        self.time_day_graph(df, axes, "pc_time_end_measurement", "diffuse_integral", 
                            sunrise_sunset=sunrise_sunset, 
                            show_xlabels=show_xlabels, show_cbar=show_cbar)
        axes.set_ylabel(self.diffuse_name+"(W/m²)")
    
    def dni(self, axes, df, sunrise_sunset=None, 
            show_xlabels:bool=True, show_cbar:bool=True):
        """graphs a time/day plot for dni
        params:
            axes: the axes to plot on
            df: the data to be plotted
            sunrise_sunset: times of sunrise and sunset for every day
            show_xlabels: wether or not to show labels on the x axis, useful when plotting multiple at once
            show_cbar: wether or not to show a colorbar, useful when plotting multiple at once
        """
        self.time_day_graph(df, axes, "pc_time_end_measurement", "direct_normal_integral", 
                            sunrise_sunset=sunrise_sunset, 
                            show_xlabels=show_xlabels, show_cbar=show_cbar)
        axes.set_ylabel("DNI(W/m²)")

        
    
    def graph_all(self, axes, df, fig, show_cbar=True, flags=None, timedelta=None, plot_sunrise_sunset=True):
        """plots all the possible graphs of this type
        params:
            axes: list of axes that the graphs will be plotted on
            df: the data to be plotted
            fig: the figure all the graphs are plotted on, used for drawing the colormap
            show_cbar: wether or not to show a colorbar, useful when plotting multiple at once
            flags: dataframe of the flagged status of the data
            timedelta: pandas timedelta representing the timezone of the data
            plot_sunrise_sunset: wether or not to plot sunrise and sunset times
        """
        self.fig = fig
        self.flags = flags
        
        sunrise_set = None
        if plot_sunrise_sunset:
            sunrise_set = graphUtils.calculate_sunrise_sunset(df[["pc_time_end_measurement", "gps_longitude", "gps_latitude", "gps_altitude"]], timedelta)
        
        # TODO: check relevant columns are in the df
        self.ghi(axes[0], df[self.requirements["ghi"]], sunrise_sunset=sunrise_set, show_xlabels=False, show_cbar=False)
        self.diff(axes[1], df[self.requirements["diff"]], sunrise_sunset=sunrise_set, show_xlabels=False, show_cbar=False)
        self.dni(axes[2], df[self.requirements["dni"]], sunrise_sunset=sunrise_set, show_xlabels=True, show_cbar=False)
        
        if show_cbar:
            graphUtils.cbar(axes, fig, self.max_integral, 100)
        
        