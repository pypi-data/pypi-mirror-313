# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import datetime

import numpy as np
import pandas as pd
import matplotlib

import hsr1.utils.HSRFunc as HsrFunc
from hsr1.plots import graphUtils


class SpectrumGraph:
    def __init__(self, cmap=None, timedelta=pd.Timedelta(0), spectrometer_average_period=60):
        self.cmap = cmap
        self.timedelta = timedelta
        self.spectrometer_average_period = spectrometer_average_period
        self.requirements = {"all":["pc_time_end_measurement", "global_spectrum", "diffuse_spectrum", "sza", "azimuth", "toa_hi"],
                             "ghi":["pc_time_end_measurement", "global_spectrum", "sza", "azimuth", "toa_hi"],
                             "diff":["pc_time_end_measurement", "diffuse_spectrum", "sza", "azimuth", "toa_hi"],
                             "dni":["pc_time_end_measurement", "global_spectrum", "diffuse_spectrum", "sza", "azimuth", "toa_hi"]}
        self.first_time = pd.to_datetime("00:00:00")
        self.last_time = pd.to_datetime("23:59:59")
        self.fig = None
    
    def spectrum_graph(self, df:pd.DataFrame, data_col:str, axes, max_reading, cbar=True, output_location=None):
        if len(df) == 0:
            return
        
        df = df.copy()
        df["pc_time_end_measurement"] = df["pc_time_end_measurement"].dt.tz_localize(None)
        first_date_reading = df["pc_time_end_measurement"].iloc[0].date()
        last_date_reading = df["pc_time_end_measurement"].iloc[len(df)-1].date()
        df = df[np.logical_and(df["pc_time_end_measurement"]>=datetime.datetime.combine(first_date_reading, self.first_time), 
                               df["pc_time_end_measurement"]<=datetime.datetime.combine(last_date_reading, self.last_time))]
        
        if len(df) == 0:
            return
    
        bbox = axes.get_window_extent()
        vert_pixels = int(bbox.height)
        horiz_pixels = int(bbox.width)
        
        
        
        pc_time_secs = (df["pc_time_end_measurement"].dt.tz_localize(None).astype("int64")/10**9).values.astype(int)
        
        first_timestamp = df["pc_time_end_measurement"].iloc[0]
        last_timestamp = df["pc_time_end_measurement"].iloc[-1]
        first_date = first_timestamp.date()
        last_date = last_timestamp.date()
        left_xlim = graphUtils.total_seconds(datetime.datetime.combine(first_date, self.first_time))
        right_xlim = graphUtils.total_seconds(datetime.datetime.combine(last_date, self.last_time))
        
        periods_in_dataset = ((right_xlim-left_xlim)//self.spectrometer_average_period)+1
        num_bins = int(min(periods_in_dataset, horiz_pixels))
        
        pixels = np.linspace(left_xlim, right_xlim, num_bins).astype(int)
        
        full_df = pd.DataFrame()
        full_df["time"] = pixels
        full_df["data"] = [np.full(801, np.nan)]*len(pixels)
        groups = np.clip(np.digitize(pc_time_secs, pixels), 0, len(pixels)-1)
        full_df.loc[groups, "data"] = df[data_col].values
        
        data = full_df["data"].values
        data = np.stack(data).T
        
        
        
        extent = (left_xlim, 
                  right_xlim, 
                  1100, 300)
        
        image = axes.imshow(data, cmap=self.cmap, norm=None, vmin=0, vmax=max_reading, aspect="auto",
                            interpolation="nearest", extent=extent)
        
        axes.set_ylabel(data_col)
        
        axes.set_xlim(left_xlim, right_xlim)
        
        if first_date == last_date:
            xticks, xlabels = self.generate_hour_xticks(first_date, last_date)
            axes.set_xticks(xticks, xlabels)
        else:
            xticks = axes.get_xticks()
            xticks = xticks[np.logical_and(xticks>=left_xlim, xticks<=right_xlim)]
            xlabels = []
            for i in range(len(xticks)):
                xlabels.append(datetime.datetime.fromtimestamp(xticks[i]).time())
            axes.set_xticks(xticks, xlabels)
        
        if cbar:
            self.add_colourmap(axes, max_reading, max(1, max_reading//5))
    
    def supplementary_integral_plot(self, data, axes, first_time, last_time, day, spec_day, cmap=False):
        ##### plot line graph of global and diffuse integral
        data = data.copy()
        data = data[["pc_time_end_measurement", "global_integral", "diffuse_integral"]].copy()
        data["pc_time_end_measurement"] = data["pc_time_end_measurement"].dt.tz_localize(None)
        first_date_reading = data["pc_time_end_measurement"].iloc[0].date()
        last_date_reading = data["pc_time_end_measurement"].iloc[len(data)-1].date()
        left_xlim = datetime.datetime.combine(first_date_reading, first_time)
        right_xlim = datetime.datetime.combine(last_date_reading, last_time)
        data = data[np.logical_and(data["pc_time_end_measurement"]>=left_xlim, 
                                   data["pc_time_end_measurement"]<=right_xlim)]
        
        pc_time_secs = (data["pc_time_end_measurement"].astype("int64")/10**9).values.astype(int)
        axes[3].plot(pc_time_secs, data["global_integral"], label="global integral")
        axes[3].plot(pc_time_secs, data["diffuse_integral"], label="diffuse integral")
        axes[3].legend()
        xticks, xlabels = spec_day.generate_hour_xticks(day, day)
        axes[3].set_xticks(xticks, xlabels)
        
        axes[3].set_xlim(graphUtils.total_seconds(left_xlim), graphUtils.total_seconds(right_xlim))
        
        if cmap:
            spec_day.add_colourmap(axes[3], 0, invisible=True)
    
    def add_colourmap(self, axes, max_reading, gap=0.5, invisible=False):
        shrink = 1 if not invisible else 0.0001
        cbar = self.fig.colorbar(matplotlib.cm.ScalarMappable(cmap="jet"), ax=axes, aspect=25, pad=0.01, shrink=shrink)
        yticks = np.arange(0, max_reading, gap)
        ytick_location = yticks/max_reading
        ytick_location[ytick_location == np.inf] = 0
        cbar.ax.set_yticks(ytick_location, yticks)
    
    def generate_hour_xticks(self, first_date, last_date):
        first_timestamp_hour = datetime.datetime.combine(first_date, datetime.time(hour=self.first_time.hour+1))
        last_timestamp_hour = datetime.datetime.combine(last_date, datetime.time(hour=self.last_time.hour))
        hours = pd.date_range(first_timestamp_hour, last_timestamp_hour, freq="1h")
        xticks = []
        xlabels = []
        for hour in hours:
            xticks.append(hour.timestamp())
            xlabels.append(hour.hour)
        xticks = np.array(xticks)
        xlabels = np.array(xlabels)
        return xticks, xlabels
    
    
    def direct_normal_spectrum(self, data:pd.DataFrame, axes, max_reading):
        self.spectrum_graph(data, "direct_normal_spectrum", 
                            axes, max_reading, True)
    
    def global_spectrum(self, data, axes, max_reading):
        self.spectrum_graph(data, "global_spectrum", 
                            axes, max_reading, True)
    
    def diffuse_spectrum(self, data, axes, max_reading):
        self.spectrum_graph(data, "diffuse_spectrum", 
                            axes, max_reading, True)
    
    
    def plot_all(self, data, axes_list):
        self.global_spectrum(data, axes_list[0], 2)
        self.diffuse_spectrum(data, axes_list[1], 10)
        self.direct_normal_spectrum(data, axes_list[2], 2)
        
        
    
    
    def plot_all_aod(self, data, axes_list, max_reading):
        self.spectrum_graph(data, "total_od", axes_list[0], max_reading, False)
        self.spectrum_graph(data, "aod_microtops", axes_list[1], max_reading, False)
        self.spectrum_graph(data, "aod_wood_2017", axes_list[2], max_reading, False)
        
        cbar = self.fig.colorbar(matplotlib.cm.ScalarMappable(cmap="jet"), ax=axes_list, aspect=25, pad=0.01)
        yticks = np.arange(0, max_reading, 0.5)
        ytick_location = yticks/max_reading
        ytick_location[ytick_location == np.inf] = 0
        cbar.ax.set_yticks(ytick_location, yticks)