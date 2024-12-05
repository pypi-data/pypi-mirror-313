# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import math
import datetime

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

from hsr1.plots import graphUtils

class DailyHists:
    def __init__(self, data, fig=None):
        data = data.copy()
        data["pc_time_end_measurement"] = data["pc_time_end_measurement"].dt.tz_localize(None)
        dates = data["pc_time_end_measurement"].dt.date
        np_dates = dates.to_numpy()
        np_dates.sort()
        dates = pd.Series(np_dates)
        data["pc_time_end_measurement"] = pd.DatetimeIndex(dates)
        
        self.dates = dates
        self.data = data
        
        self.fig = fig
        
        ##### weight each day to the number of readings in the day
        weights = []
        for date in dates.unique():
            ##### TODO: \/\/ slow!
            readings = dates.loc[dates==date]
            weights += [8640/len(readings)]*(len(readings))
        
        self.weights = np.array(weights)
        
        
        self.first_date = str(dates[0])
        self.last_date = str(dates[len(dates)-1])
        self.date_range = len(pd.date_range(self.first_date, self.last_date, freq="D"))
    
    
    def plot_hists(self, columns, title, ignore_zero=False, weight=False, **kwargs):
        """plots several hists on one page
        params:
            columns: list of columns names to plot, OR string of one column name
            title: title of the plot
            ignore_zero: filters out all the zero values
            weight: weights each column of the histogram based on how many readings are in that day
                    means shorter days have the same impact as longer days        
        """
        fig, axes = plt.subplots(len(columns), figsize=(16.5, 11.7))
        fig.suptitle(title)
        fig.tight_layout()
        
        if len(columns) == 1:
            self.plot_one_hist(columns[0], axes, ignore_zero, weight=weight, **kwargs)
        else:
            for i, column in enumerate(columns):
                self.plot_one_hist(column, axes[i], ignore_zero, weight=weight, **kwargs)
    
    def plot_one_hist(self, column, axes, 
                      ignore_zero:bool=False,
                      weight:bool=True,
                      bins=None,  
                      zero_axes:bool=False, 
                      ylims:(int, int)=None, 
                      show_xticks:bool=True, 
                      log:bool=False,
                      ybuffer:bool=False,
                      limited_bins:bool=False,
                      linthresh:int=10,
                      **kwargs):
        """plots a single histogram on the given axes
        params:
            column: the column in the dataframe that is being plotted
            axes: the axes that the histogram is being plotted on
            ignore_zero: filters out all the zero values
            weight: weights each column of the histogram based on how many readings are in that day
                    means shorter days have the same impact as longer days
            bins: number of bins to have on the y-axis
            zero_axes: if True, starts the y-axis from 0, rather than the lowest data value
            ylims: can manually set the ylims
            show_xticks: wether or not to show labels on the x-axis, usefull when plotting multiple at once with the same scale
            log: if true, uses a log scale in the positive and negative direction
            ybuffer:  if true, adds a 10% buffer to the top of the graph
            limited_bins: if true, sets the number of bins to the number of unique readings
            
            linthresh: when using a log scale, how far on either side of zero to have a linear scale rather than log
        """
        data = self.data.copy()
        
        # data["pc_time_end_measurement"] = data["pc_time_end_measurement"].dt.tz_localize(None)
        
        weights = self.weights
        not_nan = data[column].isna()
        data = data.loc[~not_nan]
        weights = weights[~not_nan]
        
        column_data = data[column].to_numpy()
        
        ##### if all the data is the same value
        one_value = len(np.unique(column_data)) == 1
        
        ybin = bins
        non_zero_df = data[column]#.replace(0, np.nan)
        if ybin is None:
            if not non_zero_df.isnull().all():
                ##### min bin is 10, max is 100
                
                space_covered = max(10, int((np.nanmax(non_zero_df)-np.nanmin(non_zero_df))*1000))
                ybin = min(100, space_covered)
            else:
                ybin = 11
            
            if limited_bins:
                data_range = np.max(non_zero_df) - np.min(non_zero_df)
                if zero_axes:
                    data_range = np.max(non_zero_df)+1
                min_diff = np.min(np.diff(np.sort(np.unique(non_zero_df))))
                
                ybin = int(data_range/min_diff)
                 
            if one_value:
                ybin = 10
        
        
        
        bins = [self.date_range, ybin]
        
        if log:
            max_mag = np.max(np.abs(column_data))
            if max_mag > linthresh:
                column_data, ylims = self.scale(axes, column_data, ylims, linthresh, **kwargs)
        
        
        
        
        
        start = datetime.datetime(1970,1,1)
        a_range = [[(data["pc_time_end_measurement"].iloc[0]-start).total_seconds()*10e8, (data["pc_time_end_measurement"].iloc[-1]-start).total_seconds()*10e8],
                  [min(column_data), max(column_data)]]
        
        if ignore_zero and ((data[column] > 0).all() or (data[column] < 0).all()):
            non_zero = ((data[column] > 0) | (data[column] < 0)).to_numpy()
            data = data.loc[non_zero]
            column_data = column_data[non_zero]
            weights = weights[non_zero]
            a_range[1][0] = min(column_data) if len(column_data) != 0 else 0
        
        if ylims is None:
            if zero_axes:
                a_range[1][0] = 0
        if ylims is not None:
            a_range[1] = [ylims[0], ylims[1]]
        
        hist = None
        if len(data) != 0:
            # if weight:
            #     hist = axes.hist2d(data["pc_time_end_measurement"], column_data, bins=bins, cmap="jet", cmin=1, range=a_range, weights=weights)
            # else:
            #     hist = axes.hist2d(data["pc_time_end_measurement"], column_data, bins=bins, cmap="jet", cmin=1, range=a_range)
            
            if weight:
                hist_array, bin_edges_x, bin_edges_y = np.histogram2d(data["pc_time_end_measurement"], column_data, bins=bins, range=a_range, weights=weights)
            else:
                hist_array, *_ = np.histogram2d(data["pc_time_end_measurement"], column_data, bins=bins, range=a_range)
            
            hist_array = hist_array.T
            hist_array = np.flip(hist_array, 0)
            hist_array[hist_array == 0.0] = np.nan
        
            extent=[a_range[0][0], a_range[0][1], a_range[1][0], a_range[1][1]]
            
            if extent[2] == extent[3]:
                extent[3] += 1
            
            if extent[0] == extent[1]:
                extent[1] += 60*1440*10e8
            
            
            hist = axes.imshow(hist_array, cmap="jet", aspect="auto", extent=extent, interpolation="none")
            
        
            xticks, labels = graphUtils.calculate_date_labels(pd.Series(pd.date_range(self.first_date, self.last_date, freq="D")), axes.get_xlim())
            if show_xticks:
                axes.set_xticks(xticks, labels)
            else:
                axes.set_xticks(xticks, [])
        
        
        
        if one_value:
            axes.set_yticks([column_data[0]], [column_data[0]])
        
        
        axes.set_ylabel(column.lstrip("_"))
        if zero_axes:
            if ylims is None:
                ylims = (0, np.max(column_data))
            else:
                ylims = (0, ylims[1])
        
        if ybuffer:
            if ylims is None:
                ylims = axes.get_ylim()
            ylims = ylims[0], ylims[1]*1.1
        
        if ylims is not None:
            axes.set_ylim(ylims[0], ylims[1])
        
        if self.fig is not None:
            self.fig.colorbar(hist, ax=axes, format="%.0f")
        
        
        
    
    def scale(self, axes, 
              column_data, 
              ylim=None, 
              linthresh=10, 
              base=10, 
              linscale=2, 
              lin_ticks=5, 
              log_ticks_skipped=0):
        """applies a symmetrical log scale to the data, and also the axes, before it gets binned"""
        sym_log_scale = matplotlib.scale.SymmetricalLogScale(None, base=base, linthresh=linthresh, linscale=linscale)
        sym_log_transform = sym_log_scale.get_transform()
        
        ##### find the max base to know how many ticks to make
        abs_max = np.max(np.abs(column_data))
        tick_max = np.emath.logn(base, abs_max)
        ##### round up to the nearest int
        tick_max = int(tick_max+1)
        
        ##### apply log trasnformation to data
        column_data = sym_log_transform.transform_non_affine(column_data)
        
        ##### generate ticks for log part of graph
        sample_yticks = np.array([base**i for i in range(tick_max+1)])
        sample_log_yticks = sample_yticks[sample_yticks > linthresh]
        sample_log_yticks_selected = sample_log_yticks[::log_ticks_skipped+1]
        
        ##### generate ticks for linear part of graph
        sample_lin_yticks = np.linspace(0, linthresh, lin_ticks).astype(int)
        
        ##### merge lin and log
        sample_yticks = np.concatenate((sample_lin_yticks, sample_log_yticks))
        
        
        ##### apply log transformation to log part of the scale and recombine with linear part
        logged_sample_log_yticks = sym_log_transform.transform_non_affine(sample_yticks)
        logged_sample_yticks = logged_sample_log_yticks
        
        ##### flip and invert for negative part
        logged_sample_yticks = np.concatenate((-np.flip(logged_sample_yticks), logged_sample_yticks))
        sample_yticks = np.concatenate((-np.flip(sample_yticks), sample_yticks))
        
        ##### format ylabels
        labels = []
        for i, tick in enumerate(sample_yticks):
            ##### if tick is part of log section
            if (tick > linthresh or tick < -linthresh):
                if tick in sample_log_yticks_selected or -tick in sample_log_yticks_selected:
                    _tick = tick
                    prefix = ""
                    if tick <= -linthresh:
                        prefix = "-"
                        _tick = -tick
                        
                    power = math.log(_tick, base)
                    labels.append(prefix+str(base)+graphUtils.superscript(int(round(power))))
                else:
                    labels.append("")
            else:
                labels.append(str(tick))
        
        if ylim is None:
            ylim = (min(column_data), max(column_data))
            ylim = (min(0, ylim[0]), max(0, ylim[1]))
            ylim = np.array(ylim)
        else:
            ylim = sym_log_transform.transform_non_affine(np.array(ylim))
        
        
        ##### apply calculated yticks using their before log values as labels  
        axes.set_yticks(logged_sample_yticks, labels)
        
        return column_data, ylim
    
    
    