# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd

import time

import hsr1.plots.graphUtils as graphUtils

class ElvAziGraph:
    def __init__(self, cmap=plt.get_cmap("jet"), diffuse_name="dif"):
        self.diffuse_name = diffuse_name
        self.cmap = cmap
        ##### according to brsn limits, highest possible global value is 1407
        self.max_integral = None
        self.requirements = {"ghi":["pc_time_end_measurement", "sza", "azimuth", "global_integral"],
                             "diff":["pc_time_end_measurement", "sza", "azimuth", "diffuse_integral"],
                             "dni":["pc_time_end_measurement", "sza", "azimuth", "direct_normal_integral"],
                             "horizon_line":["gps_latitude", "gps_longitude", "gps_altitude"],
                             "all":["pc_time_end_measurement", "sza", "azimuth", "diffuse_integral", "global_integral", "direct_normal_integral", "gps_latitude", "gps_longitude", "gps_altitude"]}
        self.flags = None
    
    
    def __calc_horizon_line(self, location):
        """reads the horizon line data
        from: https://github.com/AssessingSolar
        params:
            location: [lat, lon, elv]
        """
        import uuid
        import os
        import pandas
        from urllib.request import urlopen

        if (len(location) == 2):
            location[3] = -999;

        #unique id
        uid = uuid.uuid4().hex

        fic_output_csv = 'horizon_srtm_output_{}.csv'.format(uid)
        str_wps = 'http://toolbox.webservice-energy.org/service/wps?service=WPS&request=Execute&identifier=compute_horizon_srtm&version=1.0.0&DataInputs=';
        datainputs_wps = 'latitude={:.6f};longitude={:.6f};altitude={:.1f}'\
    	.format(location.iloc[0], location.iloc[1], location.iloc[2]);
        
        response = urlopen('{}{}'.format(str_wps,datainputs_wps))
        HZ = pandas.read_csv(response,delimiter=';',comment='#',header=None,skiprows=16,nrows=360,names=['AZIMUTH', 'ELEVATION'])
        
        if HZ["ELEVATION"].iloc[0] == np.nan:
            raise Exception("could not calcuate horizon line")
        
        return HZ
        
    
    def elv_azi_graph(self, 
                      axes,
                      df:pd.DataFrame, 
                      column_name:str, 
                      show_xlabels:bool=True, 
                      show_ylabels:bool=True,
                      show_cbar:bool=True, 
                      show_horizon=False):
        """plots a graph of elevation against azimuth with the intensity shown by colour
        params:
            axes: the axes to be plotted onto
            df: the data to be plotted
            column_name: the name of the column containing the data to be plotted
            show_xlabels: whether or not to show the x axes labels. useful when plotting multiple of these graphs with the same labels
            show_cbar: whether or not to show the colorbar. useful when plotting multiple of these graphs with the same colormap
        """
        ##### copy to have local scope
        df = df.copy()
        
        if self.max_integral is None:
            self.max_integral = np.max(df[column_name])
        
        
        bbox = axes.get_window_extent()
        vert_pixels = int(bbox.height)
        horiz_pixels = int(bbox.width)
        
        
        df["elv"] = 90-np.degrees(df["sza"])
        df["azimuth"] = np.degrees(df["azimuth"])
        
        daytime = df["elv"] >= 0
        elv = np.round(df["elv"][daytime]).astype(int)
        azi = np.round(df["azimuth"][daytime]).astype(int)
        
        if len(elv) == 0:
            return None
        
        ##### filter out nighttime
        df = df.loc[df["elv"] >= 0]
        
        ##### rounds the data to the nearest int, selects the max irradiance value, and stores them as a 2D array
        new_df = df[column_name].groupby([df["azimuth"].round(0), df["elv"].round(0)]).max().unstack(level=0).sort_index(ascending=False)
        
        new_index = np.arange(0, max(elv)+1)
        new_cols = np.arange(min(azi), max(azi)+1)
        new_df = new_df.reindex(index=np.flip(new_index), columns=new_cols)
        
        
        extent = (min(azi), max(azi), 0, max(elv))
        im = axes.imshow(new_df, aspect="auto", interpolation="none", cmap="jet", extent=extent, vmin=0, vmax=self.max_integral)
        
        
        if self.flags is not None:
            colordict = {
                "red":((0,1,1), (1,1,1)),
                "green":((0,1,1), (1,0,0)),
                "blue":((0,1,1), (1,1,1))}
            flag_cmap = LinearSegmentedColormap("LinearCmap", colordict)
            
            any_flags = pd.DataFrame()
            any_flags["flags"] = self.flags.any(axis=1)
            
            new_df = any_flags["flags"].groupby([df["azimuth"].round(0), df["elv"].round(0)]).any().unstack(level=0).sort_index(ascending=False)
            
            new_index = np.arange(0, max(elv)+1)
            new_cols = np.arange(min(azi), max(azi)+1)
            new_df = new_df.reindex(index=np.flip(new_index), columns=new_cols)
            
            new_df = new_df.astype(float).fillna(0)
            
            ##### alpha controls the transparancy of the image, this sets alpha to be opaque when flagged, and transparent when not
            ##### removes noise on the original graph
            alpha = new_df.values.astype(float)
            im = axes.imshow(new_df, aspect="auto", norm=matplotlib.colors.LogNorm(vmin=0, vmax=1), alpha=alpha, interpolation="none", cmap=flag_cmap, extent=extent)
        
        
        ylim = axes.get_ylim()
        axes.set_ylim(ylim[0], ylim[1]*1.05)
        
        if show_ylabels:
            axes.set_ylabel("solar elevation(°)")
        
        xticks = np.linspace(extent[0], extent[1], 5)
        if show_xlabels:
            axes.set_xlabel("solar azimuth(°)")
            axes.set_xticks(xticks)
        else:
            axes.set_xticks(xticks, labels=[])
        
        if show_cbar:
            self.fig.colorbar(im, ax=axes, pad=0)
    
        if show_horizon:
            ##### plots the horizon line onto the graph
            try:
                horizon_line = self.__calc_horizon_line(df.loc[0, ["gps_latitude", "gps_longitude", "gps_altitude"]])
                if type(horizon_line["AZIMUTH"].iloc[0]) != type(""):
                    axes.plot(horizon_line["AZIMUTH"], horizon_line["ELEVATION"])
                else:
                    print("invalid horizon")
            except:
                print("horizon could not be calculated")
        
        
        return im
    
    
    def ghi(self, axes, df:pd.DataFrame, show_xlabels:bool=True, show_ylabels:bool=True, show_cbar=True, show_horizon=True):
        """graphs an elevation/azimuth plot for ghi
        params:
            axes: the axes to plot on
            df: the data to be plotted
            show_xlabels: wether or not to show labels on the x axis, useful when plotting multiple at once
            show_cbar: wether or not to show a colorbar, useful when plotting multiple at once
        """
        self.elv_azi_graph(axes, df, "global_integral", show_xlabels=show_xlabels, show_ylabels=show_ylabels, show_cbar=show_cbar, show_horizon=show_horizon)
        mirror_axes = axes.twinx()
        mirror_axes.set_yticks([])
        mirror_axes.set_ylabel("GHI(W/m²)")
        
        
    
    def diff(self, axes, df:pd.DataFrame, show_xlabels:bool=True, show_ylabels:bool=True, show_cbar=True, show_horizon=True):
        """graphs an elevation/azimuth plot for diffuse
        params:
            axes: the axes to plot on
            df: the data to be plotted
            show_xlabels: wether or not to show labels on the x axis, useful when plotting multiple at once
            show_cbar: wether or not to show a colorbar, useful when plotting multiple at once
        """
        self.elv_azi_graph(axes, df, "diffuse_integral", show_xlabels=show_xlabels, show_ylabels=show_ylabels, show_cbar=show_cbar, show_horizon=show_horizon)
        mirror_axes = axes.twinx()
        mirror_axes.set_yticks([])
        mirror_axes.set_ylabel(self.diffuse_name+"(W/m²)")
        
    
    def dni(self, axes, df:pd.DataFrame, show_xlabels:bool=True, show_ylabels:bool=True, show_cbar=True, show_horizon=True): 
        """graphs an elevation/azimuth plot for dni
        params:
            axes: the axes to plot on
            df: the data to be plotted
            show_xlabels: wether or not to show labels on the x axis, useful when plotting multiple at once
            show_cbar: wether or not to show a colorbar, useful when plotting multiple at once
        """
        self.elv_azi_graph(axes, df, "direct_normal_integral", show_xlabels=show_xlabels, show_ylabels=show_ylabels, show_cbar=show_cbar, show_horizon=show_horizon)
        mirror_axes = axes.twinx()
        mirror_axes.set_yticks([])
        mirror_axes.set_ylabel("DNI(W/m²)")
        
    
    def graph_all(self, axes, df:pd.DataFrame, fig, flags=None, show_horizon=True):
        """plots all the possible graphs of this type
        params:
            axes: list of axes that the graphs will be plotted on
            df: the data to be plotted
            fig: the figure all the graphs are plotted on, for plotting a shared colorbar
        """
        self.fig = fig
        self.flags = flags
        hz_requirements = self.requirements["horizon_line"]
        self.ghi(axes[0], df[self.requirements["ghi"]+hz_requirements], show_xlabels=False, show_ylabels=False, show_cbar=False, show_horizon=show_horizon)
        self.diff(axes[1], df[self.requirements["diff"]+hz_requirements], show_xlabels=False, show_ylabels=True, show_cbar=False, show_horizon=show_horizon)
        self.dni(axes[2], df[self.requirements["dni"]+hz_requirements], show_xlabels=True, show_ylabels=False, show_cbar=False, show_horizon=show_horizon)
        
        graphUtils.cbar(axes, fig, self.max_integral, 100)
        