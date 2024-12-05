# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib


from hsr1.plots import graphUtils as utils
from hsr1.utils.spectrum import spectrumUtils as SpectrumUtils



class DailyDipsSummary:
    def __init__(self, timezone=None, reference_lines=None, reference_labels=None):
        self.reference_lines = reference_lines
        self.reference_labels = reference_labels
        self.timezone = timezone
        
    def plot_daily_dips_hist(self, global_spectrum, n=15, cutoff_wavelength=1000):
        global_spectrum = global_spectrum.copy()
        
        dates = global_spectrum["pc_time_end_measurement"]
        
        global_spectrum = global_spectrum["global_spectrum"].values
        
        nlargest, _ = SpectrumUtils.find_nlargest(global_spectrum, n, ["wavelengths", "prominences"], cutoff_wavelength, fill_nan=True)
        
        if len(nlargest) == 0:
            raise ValueError("no dips found")
        
        not_nan = np.logical_not(np.isnan(nlargest))
        nlargest = nlargest[not_nan]
        
        ##### generate a list of all the days in the dataset
        dates = pd.to_datetime(dates.dt.date)#.dt.tz_localize(self.timezone)
        dates_int = dates.astype("int64")
        all_dates = []
        [all_dates.append([x]*n) for x in dates_int]
        all_dates = np.array(all_dates).flatten()
        all_dates = all_dates[not_nan]
        
        
        fig = plt.figure(layout="constrained", figsize=(11.7, 8.3))
        axes = fig.subplots(1)
        
        ##### weight each day to the number of readings in the day
        weights = []
        for date in dates.unique():
            readings = dates.loc[dates==date]
            weights += [1440/len(readings)]*(len(readings)*n)
        weights = np.array(weights)
        weights = weights[not_nan]
        
        total_num_days = len(pd.date_range(min(dates), max(dates)))
        bins = (total_num_days, int((cutoff_wavelength-300)/1))
        
        ##### matplotlib dosent like when the data array is all the same and also large.
        #####   changing the all_dates variable to be 1 solves this issue.
        #####   xtick is taken from dates so is still valid
        if all_dates[0] == all_dates[-1]:
            all_dates = np.ones(len(all_dates))
            all_dates[-1] += 1
            
        
        hist, *_ = np.histogram2d(all_dates, nlargest, bins=bins, weights=weights, range=[[all_dates[0], all_dates[-1]], [300, bins[1]+300]])
        hist = hist.T
        hist = np.flip(hist, 0)
        hist[hist == 0.0] = np.nan
        
        extent = (all_dates[0], all_dates[-1], 300, bins[1]+300)
        image = axes.imshow(hist, cmap="jet", vmin=1, aspect="auto", extent=extent, interpolation="none")        
        
        axes.set_ylim(300, cutoff_wavelength)
        
        xticks, xlabels = utils.calculate_date_labels(dates, axes.set_xlim())
        axes.set_xticks(xticks, xlabels)
        
        # cbar = fig.colorbar(hist[3], ax=axes, aspect=25, pad=0.01)
        cbar = fig.colorbar(image, ax=axes, aspect=25, pad=0.01)
        
        utils.plot_reference_lines_and_labels(axes, all_dates[0], self.reference_lines, self.reference_labels)
        
        
        axes.set_ylabel("Wavelength, \nDip Locations from SMARTS")
        
        return fig
    
    
    def plot_daily_peaks_summary(self, global_spectrum, n, cutoff_wavelength):
        fig = self.plot_daily_dips_hist(global_spectrum, n, cutoff_wavelength)
        
        return fig