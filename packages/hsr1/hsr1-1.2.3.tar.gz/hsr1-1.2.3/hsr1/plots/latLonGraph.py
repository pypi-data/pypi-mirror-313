# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
from datetime import datetime

import numpy as np


class LatLonGraph:
    def __init__(self, data):
        self.data = data.copy()
    
    
    def bin_data(self, data, bins=None):
        """bins a series of data
        generates a list of values across the dataset, and rounds each value to 
        the closest bin
        
        params:
            data: the dataset to be binned
            bins: the number of bins to be created
        returns:
            result: the original dataset, rounded into the new bins
            bin_centres: the locations of the bins
        """
        
        ##### generates the centre of the bins
        bin_centres = np.linspace(min(data), max(data), num=bins)
        
        ##### make a 2d array of the distance between every measured point and the centre of each bin
        distances = np.abs(np.subtract.outer(bin_centres, data.to_numpy()))
        
        ##### find the index of the closest bin
        indecies = np.argmin(distances, axis=0)
        
        ##### apply the index to match the bin to where the actual value was
        result = bin_centres[indecies]
        return result, bin_centres

    
    def plot_lat_lon(self, axes, column=None, stack_resolution="max", lat_lon_name=["Latitude", "Longitude"], bins=100, title=None):
        """plots a track of the location of the dataset, with another column as the colour
        params:
            axes: the axes the graph will be plotted on
            column: the name of the column that will be plotted as colour, None=density
            stack_resolution: what to do when multiple datapoints are in the same bin
                            options: "max", "min", "mean", "mode", "first", "count"
            lat_lon_name: what the latitude and longitude are called in the dataframe
            bins: how many bins to put the data into
        """
        if title is None:
            if column is None:
                title = "Location Density"
            else:
                title = column
        
        lat_name = lat_lon_name[0]
        lon_name = lat_lon_name[1]
        
        ##### generate the bins, if there are fewer unique datapoints than bins, use number of datapoints or spread with 0.1 increments, whichever is smaller
        #####   max is 100
        new_bins = [bins, bins]
        
        lat_unique = len(self.data[lat_name].unique())
        lon_unique = len(self.data[lon_name].unique())
        
        if lon_unique < bins:
            evenly_spaced_lon = int(max(((self.data[lon_name])-min(self.data[lon_name]))/0.01)+1)
            new_bins[0] = min(100, max(lon_unique, evenly_spaced_lon))
        if lat_unique < bins:
            evenly_spaced_lat = int(max(((self.data[lat_name])-min(self.data[lat_name]))/0.01)+1)
            new_bins[1] = min(100, max(lat_unique, evenly_spaced_lat))
        
        ##### handle None column name, column dosent matter, just stack_resolution=count
        if column is None:
            column="pc_time_end_measurement"
            stack_resolution = "count"
        
        ##### load correct data from the dataframe and process if needed
        if column == "pc_time_end_measurement" or column == "density":
            self.data["data_col"] = self.data["pc_time_end_measurement"].dt.tz_localize(None).astype("datetime64[ns]").astype("int64")
        else:
            self.data["data_col"] = self.data[column]
        
        
        longitude, lon_bins = self.bin_data(self.data[lon_name], bins=new_bins[0])
        latitude, lat_bins = self.bin_data(self.data[lat_name], bins=new_bins[1])
        
        ##### group the data according to the bins, aggregate according to stack_resolution
        if stack_resolution == "max":
            new_df = self.data["data_col"].groupby([longitude, latitude]).max().unstack(level=0).sort_index(ascending=False)
        elif stack_resolution == "min":
            new_df = self.data["data_col"].groupby([longitude, latitude]).min().unstack(level=0).sort_index(ascending=False)
        elif stack_resolution == "mean":
            new_df = self.data["data_col"].groupby([longitude, latitude]).mean().unstack(level=0).sort_index(ascending=False)
        elif stack_resolution == "mode":
            new_df = self.data["data_col"].groupby([longitude, latitude]).agg(lambda x: x.value_counts().index[0]).unstack(level=0).sort_index(ascending=False)
        elif stack_resolution == "first":
            new_df = self.data["data_col"].groupby([longitude, latitude]).first().unstack(level=0).sort_index(ascending=False)
        elif stack_resolution == "count":
            new_df = self.data["data_col"].groupby([longitude, latitude]).count().unstack(level=0).sort_index(ascending=False)
        
        
        new_df = new_df.reindex(index=np.flip(lat_bins), columns=lon_bins)
        
        ##### helper function to convert string timstamps to seconds since epoch
        def str_to_epoc_s(string):
            return datetime.strptime(string, "%Y-%m-%d").timestamp()
        
        
        ##### define im here for scope
        im = None
        ##### when data is stacked, set the colourmap to range over the actual data rather than the data in the image
        if stack_resolution in ["max", "min", "mean", "first"]:
            im = axes.imshow(new_df, cmap="jet", aspect="auto", 
                             # vmin=str_to_epoc_s(np.min(self.data["pc_time_end_measurement"]).date())*10**9,
                             # vmax=str_to_epoc_s(np.max(self.data["pc_time_end_measurement"]).date())*10**9)
                             vmin=np.min(self.data["pc_time_end_measurement"]).timestamp()*10**9,
                             vmax=np.max(self.data["pc_time_end_measurement"]).timestamp()*10**9)
        else:
            im = axes.imshow(new_df, cmap="jet", aspect="auto")
        axes.set_title(title)
        
        
        self.ticks(new_bins, axes, lon_name, lat_name)
        
        return im
        
    def ticks(self, bins, axes, lon_name, lat_name):
        """adds accurate lat and lon ticks to the axes"""
        
        ##### handle when there are fewer bins than ticks,
        ##### no point having more detail on the axes than on the graph
        num_ticks = [5, 5]
        if bins[0] < num_ticks[0]:
            num_ticks[0] = bins[0]
        if bins[1] < num_ticks[1]:
            num_ticks[1] = bins[1]
        
        lon_max = np.max(self.data[lon_name])
        lon_min = np.min(self.data[lon_name])
        lonlim = axes.get_xlim()
        ##### ticks are in the middle of the bins, not the edges
        lonlim = lonlim[0]+0.5, lonlim[1]-0.5
        
        xticks = np.linspace(lonlim[0], lonlim[1], num_ticks[0])
        xlabels = np.linspace(lon_min, lon_max, num_ticks[0]).round(4)
        axes.set_xticks(xticks, xlabels)
        
        lat_max = np.max(self.data[lat_name])
        lat_min = np.min(self.data[lat_name])
        latlim = axes.get_ylim()
        ##### ticks are in the middle of the bins, not the edges
        latlim = latlim[0]-0.5, latlim[1]+0.5
        
        yticks = np.linspace(latlim[0], latlim[1], num_ticks[1])
        ylabels = np.linspace(lat_min, lat_max, num_ticks[1]).round(4)
        axes.set_yticks(yticks, ylabels)