# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from hsr1.plots import graphUtils
import hsr1.utils.spectrum.spectrumUtils as SpectrumUtils




class LinearDipsGraph:
    def __init__(self, block=True, output_location=None, title_prefix=""):
        self.block = block
        self.output_location = output_location
        self.title_prefix = title_prefix
    
    def plot_n_biggest_dips(self, global_spectrum, 
                            n=15,
                            cutoff_wavelength=1000,
                            date_format:str="%y-%m-%d %H:%M",
                            title=None):
        """one plot per day of the the n biggest peak for each measurement
        params:
            global_spectrum: dataframe containing spectral data
            n: the number of peaks that will be selected per measurement
            cutoff_wavelength: the maximum wavelength included
        """
        global_spectrum = global_spectrum.copy()
        
        dates = global_spectrum["pc_time_end_measurement"].dt.tz_localize(None)
        
        
        global_spectrum = global_spectrum["global_spectrum"].values
        
        nlargest, nlargest_width, nlargest_prominence = SpectrumUtils.find_nlargest(global_spectrum, n, ["wavelengths", "widths", "prominences"], cutoff_wavelength)        
        
        x_axis = [[i]*n for i in dates]
        x_axis = np.array(sum(x_axis, []))
        x_axis = pd.to_datetime(x_axis).astype("int64")
        xlims = (x_axis[0], x_axis[-1])
        
        ##### removing nan data
        x_axis = x_axis[~np.isnan(nlargest)]
        nlargest_width = nlargest_width[~np.isnan(nlargest)]
        nlargest_prominence = nlargest_prominence[~np.isnan(nlargest)]
        nlargest = nlargest[~np.isnan(nlargest)]
        
        ##### generate list of widths, to plot point size
        max_width = np.nanmax(nlargest_width)
        nlargest_width = ((nlargest_width/max_width)*10)**2
        
        fig, axes = plt.subplots(1, figsize=(16.5, 11.7))
        
        if title is None:
            title = str(dates.iloc[0].date())+"  -  " + str(dates.iloc[len(dates)-1].date())
        fig.suptitle("prominent dip wavelengths\n" + str(title))
        
        scatter = axes.scatter(x_axis, nlargest, s=nlargest_width, c=nlargest_prominence, cmap="jet")
        
        x_min = x_axis[0]
        x_max = x_axis[-1]
        
        x_ticks = np.linspace(x_min, x_max, 10)
        x_labels = [timestamp.strftime(date_format) for timestamp in pd.to_datetime(x_ticks)]
        
        axes.set_xticks(x_ticks, x_labels)
        
        
        axes.set_xlim(xlims)
        axes.set_ylim((300, cutoff_wavelength))
        
        graphUtils.plot_reference_lines_and_labels(axes, xlims[0])
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/"+self.title_prefix+"biggest dips graph "+str(dates.iloc[0].date())+".png")
        plt.show(block=self.block)
        
        
    
    
    def plot_biggest_dips_day(self, global_spectrum, n=15, cutoff_wavelength=1000,
                               date_format:str="%H:%M"):
        global_spectrum = global_spectrum.copy()
        global_spectrum["pc_time_end_measurement"] = pd.DatetimeIndex(global_spectrum["pc_time_end_measurement"].dt.tz_localize(None))
        
        days = global_spectrum["pc_time_end_measurement"].dt.date.unique()
        global_spectrum_days = [global_spectrum.loc[global_spectrum["pc_time_end_measurement"].dt.date == day] for day in days]
        for i, global_spectrum_day in enumerate(global_spectrum_days):
            self.plot_n_biggest_dips(global_spectrum_day, n, cutoff_wavelength, date_format="%H:%M", title=days[i])
    