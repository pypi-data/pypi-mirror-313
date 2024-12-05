# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import numpy as np
import math

from hsr1.plots import (graphUtils,
                        flagData)

class ClearnessDensityGraph:
    def __init__(self, cmap=plt.get_cmap("jet"), diffuse_name="dif"):
        self.diffuse_name = diffuse_name
        self.cmap = cmap
        ##### according to brsn limits, highest possible global value is 1407
        self.max_integral = 1407
        self.max_density = 0
        self.match_density = False
        self.requirements = {"ghi_toa":["toa_hi", "global_integral", "sed"],
                             "diff_toa":["toa_hi", "diffuse_integral", "sed"],
                             "dni_toa":["toa_hi", "direct_normal_integral", "sed"],
                             "sza_diff_ghi":["diffuse_integral", "global_integral", "sza"],
                             "ghi_dni_clearness":["global_integral", "direct_normal_integral", "toa_hi", "sza"],
                             "ghi_diff_clearness":["global_integral", "diffuse_integral", "toa_hi"],
                             "all":["toa_hi", "global_integral", "diffuse_integral", "direct_normal_integral", "sed", "sza"]}
        self.limits = flagData.calculate_limits()
        self.flag_all = False
        self.flags = pd.DataFrame()
        self.flags[["ghi_possible_min", "ghi_possible_max", "dif_possible_min", "dif_possible_max", "dni_possible_min", "dni_possible_max"]] = False
    
    
    def clearness_density_graph(self, 
                                axes, 
                                df:pd.DataFrame, 
                                x_axis:str, 
                                y_axis:str, 
                                bins=None, 
                                bin_scale:int=500, 
                                axes_range:[[float]]=None, 
                                max_density:bool=None, 
                                match_density:bool=False,
                                flags:pd.DataFrame=None):
        """plots 2 columns against each other with density shown by colour
        params:
            axes: the axes that will be plotted on
            df: dataframe containing data to be plotted
            x_axis: name of the column containing the x_axis data
            y_axis: name of the column containing the y_axis data
            bins: bins for the histogram, if none, generated using bin_scale https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist2d.html
            bin_scale: if bins = None, generate bins using this value
            axes_range: the leftmost and rightmost edges of the bins in each dimension, if none, calculated automatically
            max_density: maximum density for the colormap, used when matching density between plots
            match_density: wether or not to match the density to the max_density variable
            flags: the flags for this specific graph
        """
        df = df.copy()
        cmap = self.cmap
        
        bbox = axes.get_window_extent()
        vert_pixels = int(bbox.height)
        horiz_pixels = int(bbox.width)
        
        if bins is None:
            bins = [min(horiz_pixels, 100), min(vert_pixels, 100)]
        
        
        x_axes_data = df[x_axis].replace({np.inf:np.nan})#, np.NINF:np.nan})
        y_axes_data = df[y_axis].replace({np.inf:np.nan})#, np.NINF:np.nan})
        if axes_range is None:
            axes_range = [[np.nanmin(x_axes_data), np.nanmax(x_axes_data)], [np.nanmin(y_axes_data), np.nanmax(y_axes_data)]]
        
        hist, *_ = np.histogram2d(x_axes_data, y_axes_data, bins=bins, range=axes_range)
        
        if np.max(hist) == 0:
            print("no data to plot on hist: ", x_axis, ", ", y_axis)
            return
        
        self.max_density = max(self.max_density, np.max(hist))
        if match_density:
            if max_density == None:
                max_density = self.max_density
            else:
                self.max_density = max(self.max_density, max_density)
            max_fraction = np.max(hist)/max_density
            cmap = matplotlib.colors.LinearSegmentedColormap.from_list("new_colormap", cmap(np.linspace(0, max_fraction, 100)))
        
        extent = (axes_range[0][0], axes_range[0][1], axes_range[1][0], axes_range[1][1])
        im = axes.imshow(np.flip(hist.T, 0), aspect="auto", interpolation="none", cmap=cmap, extent=extent, norm=matplotlib.colors.LogNorm(vmin=1))
        
        xticks = axes.get_xticks()
        xlabels = axes.get_xticklabels()
        
        
        
        
        if self.flag_all:
            flag_text = str(round((sum(flags.any(axis=1))/len(df))*100, 1)) + "%"
            axes.text(0,0.88*axes.set_ylim()[1], flag_text)
            flags = self.flags
        
        if flags is not None:
            colordict = {
                "red":((0,1,1), (1,1,1)),
                "green":((0,1,1), (1,0,0)),
                "blue":((0,1,1), (1,1,1))}
            flag_cmap = LinearSegmentedColormap("LinearCmap", colordict)
            flagged_data = df.loc[flags.any(axis="columns")]
            if len(flagged_data) > 0:
                flagged_hist, *_ = np.histogram2d(flagged_data[x_axis], flagged_data[y_axis], bins=bins, range=axes_range)
                axes.imshow(np.flip(flagged_hist.T, 0), aspect="auto", interpolation="none", norm=matplotlib.colors.LogNorm(vmin=0, vmax=1), cmap=flag_cmap, extent=extent)
        
        axes.set_xticks(xticks, xlabels)
        
        return im
                
    
    def ghi_toa(self, axes, df:pd.DataFrame, match_density=None):
        """plot to compare the ghi to the top of atmosphere irradiance
        params:
            axes: the axes to plot on
            df: the data to be plotted
            match_density: wether or not to match the density to self.max_integral
        """
        ##### the flags checked by this graph
        flag_names = ["ghi_possible_min", "ghi_possible_max", "ghi_rare_min", "ghi_rare_max"]
        
        if match_density == None:
            match_density = self.match_density
        axes.plot(self.limits["toa_hi"], self.limits["ghi_possible"], color="black")
        axes.plot(self.limits["toa_hi"], self.limits["ghi_rare"], color="black")
        
        flags = None
        if not self.flags.empty:
            flags = self.flags[flag_names]
        
        im = self.clearness_density_graph(axes, df, "toa_hi", "global_integral", 
                                          axes_range=[[0,np.nanmax(df["toa_hi"])],[0,self.max_integral]], 
                                          match_density=match_density, 
                                          flags=flags)
        
        xlim = axes.get_xlim()
        axes.set_xlim(xlim[0], xlim[1]*1.05)
        
        axes.set_ylabel("GHI(W/m²)")
        axes.set_xlabel("Top of Atmosphere(W/m²)")
        
        return im
    
    def diff_toa(self, axes, df:pd.DataFrame, match_density=None):
        """plot to compare the diffuse to the top of atmosphere irradiance
        params:
            axes: the axes to plot on
            df: the data to be plotted
            match_density: wether or not to match the density to self.max_integral
        """
        ##### the flags checked by this graph
        flag_names = ["dif_possible_min", "dif_possible_max", "dif_rare_min", "dif_rare_max"]
        
        if match_density == None:
            match_density = self.match_density
        axes.plot(self.limits["toa_hi"], self.limits["diff_possible"], color="black")
        axes.plot(self.limits["toa_hi"], self.limits["diff_rare"], color="black")
        
        flags = None
        if not self.flags.empty:
            flags = self.flags[flag_names]
        
        im = self.clearness_density_graph(axes, df, "toa_hi", "diffuse_integral", 
                                          axes_range=[[0,np.nanmax(df["toa_hi"])],[0,self.max_integral]], 
                                          match_density=match_density, 
                                          flags=flags)
        
        xlim = axes.get_xlim()
        axes.set_xlim(xlim[0], xlim[1]*1.05)
        
        axes.set_ylabel(self.diffuse_name+"(W/m²)")
        axes.set_xlabel("Top of Atmosphere(W/m²)")
        
        return im
    
    def dni_toa(self, axes, df:pd.DataFrame, match_density=None):
        """plot to compare the dni to the top of atmosphere irradiance
        params:
            axes: the axes to plot on
            df: the data to be plotted
            match_density: wether or not to match the density to self.max_integral
        """
        ##### the flags checked by this graph
        flag_names = ["dni_possible_min", "dni_possible_max", "dni_rare_min", "dni_rare_max"]
        
        if match_density == None:
            match_density = self.match_density
        axes.plot(self.limits["toa_hi"], self.limits["dni_possible"], color="black")
        axes.plot(self.limits["toa_hi"], self.limits["dni_rare"], color="black")
        
        flags = None
        if not self.flags.empty:
            flags = self.flags[flag_names]
        
        im = self.clearness_density_graph(axes, df, "toa_hi", "direct_normal_integral", 
                                          axes_range=[[0,np.nanmax(df["toa_hi"])],[0,self.max_integral]], 
                                          match_density=match_density, 
                                          flags=flags)
        
        xlim = axes.get_xlim()
        axes.set_xlim(xlim[0], xlim[1]*1.05)
        
        axes.set_ylabel("DNI(W/m²)")
        axes.set_xlabel("Top of Atmosphere(W/m²)")
    
        return im
    
    
    def sza_diff_ghi(self, axes, df:pd.DataFrame, match_density=None):
        """plots the diffuse ratio against the solar zenith angle
        params:
            axes: the axes to plot on
            df: the data to be plotted
            match_density: wether or not to match the density to self.max_integral
        """
        ##### the flags checked by this graph
        flag_names = ["diffuse_ratio_sza_possible_max"]
        
        if match_density == None:
            match_density = self.match_density
        # TODO: plot uncheckable values(ghi<50)? would mean no need for cropping, but also miss out on some data
        
        ##### copy df for local scope
        new_df = df.copy()
        
        new_df["diff/ghi"] = new_df["diffuse_integral"]/new_df["global_integral"]
        new_df["deg_sza"] = np.degrees(new_df["sza"])
        
        axes_range = [[0, 90], [0, 1.4]]
        
        axes.plot(np.degrees(self.limits["SZA"]), self.limits["diff/ghi_sza_comparison"], color="black")
        
        flags = None
        if not self.flags.empty:
            flags = self.flags[flag_names]
        
        im = self.clearness_density_graph(axes, new_df, "deg_sza", "diff/ghi", 
                                          axes_range=axes_range, 
                                          match_density=match_density, 
                                          flags=flags)
        
        
        axes.set_ylabel(self.diffuse_name+"/GHI")
        axes.set_xlabel("Solar zenith angle(°)")
        
        return im
    
    def ghi_dni_clearness(self, axes, df:pd.DataFrame, match_density=None):
        """plots the dni/toani ratio against the ghi/toa ratio
        params:
            axes: the axes to plot on
            df: the data to be plotted
            match_density: wether or not to match the density to self.max_integral
        """
        ##### the flags checked by this graph
        flag_names = ["dni_toani_ghi_toa_possible_max"]
        
        if match_density == None:
            match_density = self.match_density
        
        ##### copy df for local scope
        new_df = df.copy()
        
        new_df["dni/toani"] = df["direct_normal_integral"]/(df["toa_hi"]/np.cos(df["sza"]))
        new_df["ghi/toa"] = df["global_integral"]/df["toa_hi"]
        
        axes.plot(self.limits["ghi_toa"], self.limits["dni_toani"], color="black")
        axes.vlines(1.35, 0, 0.95, colors="black")
        
        axes_range = [[0, 1.5], [0,1]]
        
        flags = None
        if not self.flags.empty:
            flags = self.flags[flag_names]
        
        im = self.clearness_density_graph(axes, new_df, "ghi/toa", "dni/toani", 
                                          axes_range=axes_range, 
                                          match_density=match_density, 
                                          flags=flags)
        
        
        axes.set_ylabel("DNI/TOANI")
        axes.set_xlabel("GHI/TOA")
        
        return im
    
    def ghi_diff_clearness(self, axes, df:pd.DataFrame, match_density=None):
        """plots the diffuse ratio against the ghi/toa ratio
        params:
            axes: the axes to plot on
            df: the data to be plotted
            match_density: wether or not to match the density to self.max_integral
        """
        ##### the flags checked by this graph
        flag_names = ["diffuse_ratio_ghi_toa"]
        
        if match_density == None:
            match_density = self.match_density
        
        ##### copy df for local scope
        new_df = df.copy()
        
        new_df["diff/ghi"] = df["diffuse_integral"]/df["global_integral"]
        new_df["ghi/toa"] = df["global_integral"]/df["toa_hi"]
        
        axes.plot(self.limits["ghi/toa"], self.limits["diff/ghi"], color="black")
        
        flags = None
        if not self.flags.empty:
            flags = self.flags[flag_names]
        
        axes_range = [[0, 1.5], [0, 1.4]]
        im = self.clearness_density_graph(axes, new_df, "ghi/toa", "diff/ghi", 
                                     axes_range=axes_range, 
                                     match_density=match_density, 
                                     flags=flags)
        
        
        axes.set_ylabel(self.diffuse_name+"/GHI")
        axes.set_xlabel("GHI/TOA")
        
        return im
        
    
    def graph_all(self, axes, df:pd.DataFrame, fig, match_density:bool=False, flags:pd.DataFrame=None, flag_all:bool=False):
        """plots all the possible graphs of this type
        params:
            axes: list of axes that the graphs will be plotted on
            df: the data to be plotted
            fig: the figure all the graphs are plotted on, for plotting a shared colorbar
            match_density: wether or not to match the density to self.max_integral
            flags: all the flags generated for the dataset
            flag_all: wether to plot all the flagged data on each graph, of just the flags from that graph
        """
        if flag_all:
            self.flag_all = True
        
        # if flags is None:
        self.flags = flags
        
        im = self.ghi_toa(axes[0], df[self.requirements["ghi_toa"]])
        self.diff_toa(axes[1], df[self.requirements["diff_toa"]])
        self.dni_toa(axes[2], df[self.requirements["dni_toa"]])
        self.sza_diff_ghi(axes[3], df[self.requirements["sza_diff_ghi"]])
        self.ghi_dni_clearness(axes[4], df[self.requirements["ghi_dni_clearness"]])
        self.ghi_diff_clearness(axes[5], df[self.requirements["ghi_diff_clearness"]])
        
        if match_density:
            fig.colorbar(im, ax=axes, aspect=25, pad=0.01)
        