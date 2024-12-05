# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
from datetime import datetime
from pathlib import Path
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import scipy as sp
import pvlib

from hsr1 import DBDriver

from hsr1.plots import (
    TimeDayGraph,
    ElvAziGraph,
    ClearnessDensityGraph,
    LinearTimeGraph,
    LinearDipsGraph,
    DailyDipsSummary,
    LatLonGraph,
    DailyPlots,
    DailyHists,
    SpectrumGraph,
    flagData)

import hsr1.plots.graphUtils as graphUtils
from hsr1.utils.reformatData import ReformatData as reformat
import hsr1.utils.HSRFunc as HsrFunc



class Graph:
    def __init__(self, 
                 driver:DBDriver=None, 
                 timezone:str="+00:00",
                 output_location:str=None, 
                 diffuse_name:str="DIF", 
                 dpi:int=100,
                 block=True,
                 **kwargs):
        """a general class for easy access to all the different graph options
        params:
            driver: a DBDriver object that contains the data that will be graphed,
                if you want to plot data from an already existing dataframe, dont pass anything here
                and pass dataframe=your_dataframe in each graph
            output_location: String filepath to a folder where all the graphs generated will be stored
            diffuse_name: what to call the diffuse on graph labels
            timezone: the desired timezone of the data, if loading from a database
            dpi: dots per inch, pixel resolution of the data
            block: whether or not matplotlib waits for the user to close a graph before generating the next one.
                if true, you will have to manually close each graph to make the program run
                if false, all the graphs will be plotted as fast as they are generated.
                note: as python dosen't wait for the user to close plots before continuing,
                when it reaches the end of the program, it will terminate, closing all the plots with it.
                if you want the plots to persist once they're all generated, call graph.wait_until_closed()
            **kwargs: keyword argurments to pass to load()
        
        this contains many examples of how the underlying graph classes in hsr1.plots
        can be used. there are combined plots with several similar graphs,
        some functions that provide a simple wrapper around a class, and some that
        load data, do some data processing, and then use one of the plots from hsr1.plots
        """
        if isinstance(driver, str):
            print("db_name was passed")
            driver = DBDriver(driver)
        self.driver = driver
        self.diffuse_name = diffuse_name
        self.output_location = output_location
        self.kwargs = kwargs
        self.timezone, self.timedelta = reformat().calculate_timezone(timezone)
        self.kwargs["timezone"] = timezone
        self.block = block
        
        self.deployment_metadata = None
        
        
        if output_location is not None:
            Path(output_location).mkdir(parents=True, exist_ok=True)
        
            
        self.jet_black_zero = self.__make_colormap()
        
        matplotlib.rcParams["figure.dpi"] = dpi
        
        SMALL_SIZE = 8
        MEDIUM_SIZE = 10
        BIGGER_SIZE = 15
        
        matplotlib.rc('font', size=MEDIUM_SIZE)
        matplotlib.rc('axes', titlesize=BIGGER_SIZE)
        matplotlib.rc('axes', labelsize=MEDIUM_SIZE)
        matplotlib.rc('xtick', labelsize=SMALL_SIZE)
        matplotlib.rc('ytick', labelsize=SMALL_SIZE)
        matplotlib.rc('legend', fontsize=SMALL_SIZE)
        matplotlib.rc('figure', titlesize=BIGGER_SIZE)
    
    
    """--------------------
    line plots and presets:
    -------------------"""
    def plot_daily_line(self, columns:[str], period="monthly", 
                        rows:int=None, days_in_row:int=None, 
                        flag:bool=False, 
                        ignore_zero:bool=False,
                        title_prefix="", dataframe=None, 
                        max_limit=None, min_limit=None):
        """loads some columns from the database and plots them as daily line graphs
        params:
            columns: list of column headers to plot
            period(int or string): how many days to plot per page, options: "weekly", "monthly", int
            rows: number of rows per page
            days_in_row: number of days per row
            flag: whether or not to superimpose flagged data onto the graphs
            ignore_zero: whether or not to plot zeros
            title_prefix: string that will display before the title
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe columns must be columns+["pc_time_end_measurement"]
            max_limit, min_limit: the limit of data that is plotted
        """
        print("plotting daily line graph")
        data_columns = columns.copy()
        
        timezone = self.timezone
        ##### calculate the dni if requested
        dni=False
        if "direct_normal_integral" in data_columns:
            dni=True
            data_columns += ["sza", "global_integral", "diffuse_integral"]
            ##### can't load the dni, as it's not in the database
            data_columns.remove("direct_normal_integral")
        
        ##### add the necessary columns for flagging
        if flag and np.isin(["global_integral", "diffuse_integral"], data_columns).any():
            data_columns += ["toa_hi", "sza"]
        
        ##### one liner to remove duplicates from a list while preserving the order
        data_columns = list(dict.fromkeys(data_columns).keys())+["pc_time_end_measurement"]
        
        data = self.load_data(data_columns, dataframe)
        
        if dni:
            data["direct_normal_integral"] = ((data["global_integral"]-data["diffuse_integral"])/np.cos(data["sza"]))
        
        if ignore_zero:
            data = data.replace({0:np.nan})
        
        ##### uses the passed value of deployment metadata as a default, 
        deployment_metadata = self.deployment_metadata
        if deployment_metadata is None and self.driver is not None:
            ##### loads everything from the deployment metadata and generates the title and description
            deployment_metadata = self.driver.db_load.load_metadata()
        
        if deployment_metadata is None:
            print("No Deployment metadata available for the title")
        else:
            title_prefix = deployment_metadata["deployment_description"][0] + "\n" + title_prefix
        
        dp = DailyPlots(columns, data, title_prefix, 
                        output_location=self.output_location, flag=flag, 
                        max_limit=max_limit, min_limit=min_limit,
                        block=self.block)
        dp.plot_series(period, rows, days_in_row, data)
        
        # if self.output_location is not None:
        #     plt.savefig(self.output_location+"/" + ", ".join(columns) + " line.png")
        plt.show(block=self.block)
    
    def daily_integrals(self, period="monthly", rows=None, days_in_row=None, flag=True, dataframe=None):
        """daily plot preset of dni, ghi, and diffuse, also uses sza and toa_hi to flag data"""
        print("plotting daily integrals")
        columns = ["direct_normal_integral", "global_integral", "diffuse_integral"]
        self.plot_daily_line(columns, period, rows, days_in_row, flag, title_prefix="sunlight intensity in ", dataframe=dataframe)
    
    def daily_temps(self, period="monthly", rows=None, days_in_row=None, flag=True, dataframe=None):
        """daily plot preset of all different temperature measurements"""
        print("plotting daily temps")
        columns = ["T_CPU", "T_Bezel", "T_RH", "T_Baro"]
        self.plot_daily_line(columns, period, rows, days_in_row, flag, True, title_prefix="temperatures in ", dataframe=dataframe)
    
    def daily_aod_cimel(self, aod_type:str="aod_microtops", wavelengths:list=None, 
                        period="monthly", rows=None, days_in_row=None, 
                        upper_limit=1, lower_limit=0,
                        clearsky_filter:str="wood", clearsky_filter_kwargs:dict={},
                        dataframe=None):
        """daily plot of the aod at the wavelengths measured by cimel spectrometers
        these wavelengths are: [380, 440, 500, 675, 870, 1020]
        
        params:
            aod_type: one of: total_od, aod_microtops, aod_wood_2017
                which aod calculation to use.
            period(int or string): how many days to plot per page, options: "weekly", "monthly", int
            rows: number of rows per page.
            days_in_row: number of days per row.
            upper_limit: the max value to display.
            lower_limit: the minimum value to display.
            clearsky_filter: which clearsky filter algorithm to use.
            clearsky_filter_kwargs: keyword arguments to pass to clearsky_filter.
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "global_spectrum", "diffuse_spectrum", "sza", "sed", "global_integral", "diffuse_integral"]
        """
        print("plotting aod at cimel wavelengths")
        cimel_wavelengths=False
        if wavelengths is None:
            cimel_wavelengths=True
            wavelengths = np.array([380, 440, 500, 675, 870, 1020])
        else:
            wavelengths = np.array(wavelengths)
        
        columns = ["pc_time_end_measurement", "global_spectrum", "diffuse_spectrum", "sza", "sed", "global_integral", "diffuse_integral"]
        data = self.load_data(columns, dataframe)
        
        data = data.drop_duplicates(["pc_time_end_measurement"])
        
        deployment_metadata = None
        if self.deployment_metadata is None and self.driver is not None:
            deployment_metadata = self.driver.load_metadata()
        else:
            deployment_metadata = self.deployment_metadata
        
        if deployment_metadata is not None:
            title = deployment_metadata["deployment_description"][0] + "\n"
        
        aod_data = HsrFunc.calc_aod_from_df(data, cimel_wavelengths)
        aod_data[["global_integral", "diffuse_integral", "sza"]] = data[["global_integral", "diffuse_integral", "sza"]]
        
        aod = np.stack(aod_data[aod_type].values)[:, wavelengths-300] if not cimel_wavelengths else aod_data[aod_type].values
        
        clearsky_filter = HsrFunc.calculate_clearsky_filter(data, method=clearsky_filter, kwargs=clearsky_filter_kwargs)
        aod = aod[clearsky_filter]
        time_col = aod_data["pc_time_end_measurement"][clearsky_filter].reset_index(drop=True)
        
        limited_df = pd.DataFrame(list(aod), columns=wavelengths.astype(str))
        limited_df["pc_time_end_measurement"] = time_col
        
        self.plot_daily_line(wavelengths.astype(str), 
                             period, rows, days_in_row, 
                             dataframe=limited_df, 
                             max_limit=upper_limit, min_limit=0, 
                             title_prefix=aod_type+"\n")
        
        
    """-------------------
    hist plots and presets
    -------------------"""
    
    def plot_daily_hist(self, columns:[str], title:[str]="", dataframe=None, **kwargs):
        """plots a histogram of each column, one column per day
        params:
            columns: list of column headers that will be plotted
                    OR string of one column name
            title: the title of the plot
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                columns+["pc_time_end_measurement"]
        """
        print("plotting daily histograms")
        if type(columns) == str:
            columns = [columns]
        
        data = self.load_data(columns+["pc_time_end_measurement"], dataframe)
        
        dh = DailyHists(data)
        dh.plot_hists(columns, title, **kwargs)
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/daily hist graph.png")
        plt.show(block=self.block)
    
    def voltage_hists(self, dataframe=None):
        """daily histogram preset of all voltage measurements"""
        print("plotting voltage histograms")
        columns = ["_15Vin", "_3VCAP", "Vcc", "VSpare"]
        data = self.load_data(columns, dataframe)
        
        data[columns] /= 1000
        dh = DailyHists(data)
        dh.plot_hists(columns, "Voltages (x1000)", ignore_zero=True)
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/voltage hist graph.png")
        plt.show(block=self.block)
        
    def pht_hists(self, dataframe=None):
        """daily histogram preset of pressure, humidity and temperature"""
        print("plotting temperature, pressure, and humidity histograms")
        columns = ["pressure", "rh", "baro_temp"]
        data = self.load_data(columns, dataframe)
        
        dh = DailyHists(data)
        dh.plot_hists(columns, "Pressure, humidity and temperature", ignore_zero=True)
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/pressure, humidity and temperature graph.png")
        plt.show(block=self.block)
    
    def current_hists(self, dataframe=None):
        """daily histogram preset of all current measurements"""
        print("plotting current histograms")
        
        columns = ["I_Tot", "I_15VCAM", "I_15VPC", "ISpare"]
        data = self.load_data(columns, dataframe)
        
        dh = DailyHists(data)
        dh.plot_hists(columns, "Currents", ignore_zero=False)
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/currents hist graph.png")
        plt.show(block=self.block)
    
    
    """---------
    custom plots
    --------"""
    
    def biggest_dips(self, n=15, cutoff_angle=np.radians(80), cutoff_wavelength=1000,
                      date_format:str="%y-%m-%d %H:%M",
                      dataframe=None):
        """whole dataset plot of the n biggest peaks for each measurement, looks like several horizontal lines
        params:
            n: the number of peaks that will be selected per measurement
            cutoff_angle = the maximum zenith angle included, used for excluding nighttime
            cutoff_wavelength: the maximum wavelength included
            date_format: the format that dates will be displayed. in the same format as strftime
                https://docs.python.org/3/library/datetime.html
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "global_spectrum"]
        """
        print("plotting the biggest dips")
        if dataframe is None:
            dataframe = self.load_spectrum(cutoff_angle, **self.kwargs)
        
        linearDipsGraph = LinearDipsGraph(block=self.block, output_location=self.output_location, title_prefix="full dataset ")
        linearDipsGraph.plot_n_biggest_dips(dataframe, n, cutoff_wavelength)
    
    def daily_biggest_dips(self, n:int=15, cutoff_angle:float=np.radians(80), 
                            cutoff_wavelength:int=1000,
                            date_format:str="%H:%M",
                            dataframe=None):
        """one plot per day of the the n biggest peaks for each measurement
        params:
            n: the number of peaks that will be selected per measurement
            cutoff_angle = the maximum zenith angle included, used for excluding nighttime
            cutoff_wavelength: the maximum wavelength included
            date_format: the format that dates will be displayed. in the same format as strftime
                https://docs.python.org/3/library/datetime.html
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "global_spectrum"]
        """
        print("plotting the biggest dips in each day")
        if dataframe is None:
            dataframe = self.load_spectrum(cutoff_angle, **self.kwargs)
        
        linearDipsGraph = LinearDipsGraph(block=self.block, output_location=self.output_location)
        linearDipsGraph.plot_biggest_dips_day(dataframe, n, cutoff_wavelength, date_format)
        
        
    
    def plot_time_day(self, column:str, stack_resolution="max", max_integral=2, dataframe=None):
        """plots a column from the database on a time/day plot
        params:
            column: the column to plot
            stack_resolution: how to resolve conflicts where there are more readings than pixels
                options="max", "mean", "min"
            max_integral: the max value that the colourmap extends over
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                [column, "pc_time_end_measurement"]
        """
        print("plotting a time/day graph")
        columns = [column]+["pc_time_end_measurement"]
        data = self.load_data(columns, dataframe)
        
        fig = plt.figure(figsize=(11.7, 8.3))
        axes = fig.subplots(1)
        td = TimeDayGraph(self.jet_black_zero, max_integral)
        td.fig = fig
        td.time_day_graph(data, axes, "pc_time_end_measurement", column, 
                          stack_resolution=stack_resolution)
        axes.set_ylabel("hour of day")
        
        deployment_metadata = self.deployment_metadata
        if deployment_metadata is None:
            if self.driver is not None:
                deployment_metadata = self.driver.load_metadata()
            else:
                print("No Deployment metadata available for the title")
        
        if deployment_metadata is not None:
            title = deployment_metadata["deployment_description"][0] + "\n" + column
            plt.figtext(x=0.5, y=0.93, s=title, horizontalalignment="center")
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/time-day graph.png")
        plt.show(block=self.block)
    
    
    def plot_elv_azi(self, column:str, dataframe=None):
        """plots a graph of elevation against azimuth, with the colour representing
        the largest of a given value measured with each pair of elevation and azimuth values.
        
        currently data from accessory_datadoes not work, only data from 
            spectral_data, system_data, and precalculated_values works.
        
        params:
            column: the column that will be represented by the colourmap
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                [column, "pc_time_end_measurement", "sza", "azimuth"]
        """
        # TODO: make accessory_data work
        # truncate dosent work, assumes 1min data
        # use code from reformat_data? 
        print("plotting an elevation/azimuth graph")
        # data = self.dataframe.copy()
        # if np.logical_not(np.isin([column], data.columns)).any():
        #     data = self.driver.db_load.load([column]+["pc_time_end_measurement", "sza", "azimuth"], timezone=self.timezone, **self.kwargs)
        
        columns = [column]+["pc_time_end_measurement", "sza", "azimuth"]
        data = self.load_data(columns, dataframe)
        
        fig = plt.figure(figsize=(11.7, 8.3))
        axes = fig.subplots(1)
        elv_azi = ElvAziGraph()
        elv_azi.fig = fig
        elv_azi.elv_azi_graph(axes, data, column)
        
        deployment_metadata = self.deployment_metadata
        if deployment_metadata is None:
            if self.driver is not None:
                deployment_metadata = self.driver.load_metadata()
            else:
                print("No Deployment metadata available for the title")
        
        if deployment_metadata is not None:
            title = deployment_metadata["deployment_description"][0] + "\n" + column
            plt.figtext(x=0.5, y=0.93, s=title, horizontalalignment="center")
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/elevation-azimuth graph.png")
        plt.show(block=self.block)
    
    
    
    
    
    def plot_aod_day(self, clearsky_filter:str="wood", clearsky_filter_kwargs:dict={}, dataframe=None):
        """Plots the Aerosol Optical Depth across the spectrum, one page per day
        params:
            clearsky_filter: which clearsky filtering method to use. currently only "wood" is implemented.
                if None, no filtering is applied
            clearsky_filter_kwargs: keyword arguments to pass to the clearsky_filter method,
                these will vary depending on which filtering method is used
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "global_spectrum", "diffuse_spectrum", "sza", "sed", "global_integral", "diffuse_integral"]
        
        """
        print("plotting the aod each day")
        columns = ["pc_time_end_measurement", "global_spectrum", "diffuse_spectrum", "sza", "sed", "global_integral", "diffuse_integral"]
        data = self.load_data(columns, dataframe)
        data = data.drop_duplicates(["pc_time_end_measurement"])
        
        deployment_metadata = None
        if self.deployment_metadata is None and self.driver is not None:
            deployment_metadata = self.driver.load_metadata()
        else:
            deployment_metadata = self.deployment_metadata
        
        title=""
        spectrometer_average_period = 60
        if deployment_metadata is not None:
            title = deployment_metadata["deployment_description"][0] + "\n"
            spectrometer_average_period = float(deployment_metadata["spectrometer_average_period"][0])
        
        spec_day = SpectrumGraph(cmap=self.jet_black_zero, timedelta=self.timedelta, spectrometer_average_period=spectrometer_average_period)
        
        ##### calculate aod values
        aod_data = HsrFunc.calc_aod_from_df(data)
        aod_data[["global_integral", "diffuse_integral"]] = data[["global_integral", "diffuse_integral"]]
        
        clearsky_filter = HsrFunc.calculate_clearsky_filter(data, method=clearsky_filter, kwargs=clearsky_filter_kwargs)
        
        all_daytime_timestamps = pd.to_datetime(data.loc[data["sza"] < np.radians(90), "pc_time_end_measurement"]).dt.tz_localize(None)
        
        all_daytime_times = all_daytime_timestamps.dt.time
        first_time = np.min(all_daytime_times)
        last_time = np.max(all_daytime_times)
        
        spec_day.first_time, spec_day.last_time = first_time, last_time
        
        all_dates = all_daytime_timestamps.dt.date
        days = np.unique(all_dates)
        for day in days:
            day_data = aod_data[aod_data["pc_time_end_measurement"].dt.date == day]
            
            day_clearsky_filter = clearsky_filter[aod_data["pc_time_end_measurement"].dt.date == day]
            
            if len(day_data[day_clearsky_filter]) == 0:
                continue
            
            fig = plt.figure(figsize=(11.7, 8.3))
            
            this_title = title + "Spectral AOD data on "+day.strftime("%Y-%m-%d")
            fig.suptitle(this_title)
            
            axes = fig.subplots(4)
            
            spec_day.fig = fig
            spec_day.plot_all_aod(day_data[day_clearsky_filter].reset_index(drop=True), axes, 2)
            
            spec_day.supplementary_integral_plot(day_data, axes, first_time, last_time, day, spec_day)
            
            pc_time_secs = (data["pc_time_end_measurement"].dt.tz_localize(None).astype("int64")/10**9).values.astype(int)
            aod_500 = np.stack(aod_data["total_od"].values)[:, 500]*500
            axes[3].plot(pc_time_secs, aod_500, label="optical depth x500")
            axes[3].legend()
            
            if self.output_location is not None:
                full_title = graphUtils.make_full_title(this_title)
                plt.savefig(self.output_location+"/aod_day "+str(day)+".png")
            
            plt.show(block=self.block)
    
    def plot_spectrum_day(self, normalisation=None, dataframe=None):
        """plots each spectrum over a day on a colour intensity plot
        params:
            normalisation: how to normalise the data default None
                None: no normalisation
                toa_integral: divided by the top of atmosphere integral
                pvlib: normalises against a spectrum generated by pvlib
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["gps_latitude", "gps_longitude", "gps_altitude", "global_integral", "diffuse_integral"]
                and whatever column you are plotting. 
                if plotting direct normal, ["global_spectrum", "diffuse_spectrum", "sza"] are also required
        """
        print("plotting the spectral intensity each day")
        spec_day = SpectrumGraph(cmap=self.jet_black_zero, timedelta=self.timedelta)
        
        requirements = []
        requirements = ["gps_latitude", "gps_longitude", "gps_altitude"]
        requirements += spec_day.requirements["all"].copy()
        requirements += ["global_integral", "diffuse_integral"]
        
        data = self.load_data(requirements, dataframe)        
        
        data = data.drop_duplicates(["pc_time_end_measurement"])
        
        
        deployment_metadata = None
        if self.deployment_metadata is None and self.driver is not None:
            deployment_metadata = self.driver.load_metadata()
        else:
            deployment_metadata = self.deployment_metadata
        
        title=""
        if deployment_metadata is not None:
            title = deployment_metadata["deployment_description"][0] + "\n"
            spec_day.spectrometer_average_period = int(deployment_metadata["spectrometer_average_period"][0])
        
        data["direct_normal_spectrum"] = HsrFunc.calc_direct_normal_spectrum(data["global_spectrum"], 
                                                                             data["diffuse_spectrum"], 
                                                                             data["sza"])
        data["toa_ni"] = data["toa_hi"]/np.cos(data["sza"])
        
        if normalisation is not None and normalisation=="toa_integral":
            max_toa = np.max(data["toa_hi"])
            data["global_spectrum"] = data["global_spectrum"]/(data["toa_hi"])#/max_toa)
            data["diffuse_spectrum"] = data["diffuse_spectrum"]/(data["toa_hi"])#/max_toa)
            data["direct_normal_spectrum"] = data["direct_normal_spectrum"]/data["toa_ni"]
        elif normalisation is not None and normalisation=="pvlib":
            pvlib_data = data.copy()
            pvlib_data["sza_deg"] = np.degrees(data["sza"])
            pvlib_data["azimuth_deg"] = np.degrees(data["azimuth"])
            pvlib_data["dayofyear"] = data["pc_time_end_measurement"].dt.day_of_year
            ref_spectra = pvlib.spectrum.spectrl2(pvlib_data["sza_deg"].values, #zenith
                                                  pvlib_data["sza_deg"].values, #aoi
                                                  0, #surface_tilt
                                                  0, #ground_albedo
                                                  101325, #surface_pressure
                                                  pvlib.atmosphere.get_relative_airmass(pvlib_data["sza_deg"].values),
                                                  0.5, #precipitable_water
                                                  0.3, #atmospheric_ozone
                                                  0.1, #aerosol_turbidity
                                                  pvlib_data["dayofyear"].values)
            ref_wavelength = [ref_spectra["wavelength"]]
            
            def interp_and_divide(measured_spectra, reference_spectra):
                reference_spectra = sp.interpolate.interpn(ref_wavelength, reference_spectra, np.arange(300, 1101, 1)).T
                normalised_spectra = np.stack(measured_spectra)/reference_spectra
                normalised_spectra = np.nan_to_num(normalised_spectra, nan=0.0)
                normalised_spectra = np.array(np.split(normalised_spectra, len(normalised_spectra)))
                normalised_spectra = list(normalised_spectra[:, 0, :])
                
                return normalised_spectra
            
            data["global_spectrum"] = interp_and_divide(data["global_spectrum"].values, ref_spectra["poa_global"])
            data["diffuse_spectrum"] = interp_and_divide(data["diffuse_spectrum"].values, ref_spectra["dhi"])
            data["direct_normal_spectrum"] = interp_and_divide(data["direct_normal_spectrum"].values, ref_spectra["dni"])
            
        ##### find the max reading from the global and diffuse spectra
        #####  dni is not included as this gets very high at sunrise/sunset
        all_readings = np.array((np.stack(data.loc[data["sza"]<np.radians(80), "global_spectrum"].values), 
                                 np.stack(data.loc[data["sza"]<np.radians(80), "diffuse_spectrum"].values)))
        all_readings[np.logical_or(all_readings==np.inf, all_readings==-np.inf)] = np.nan
        all_readings = all_readings[:, :, :720]
        max_reading = np.nanmax(all_readings)
        
        all_daytime_timestamps = pd.to_datetime(data.loc[data["sza"] < np.radians(90), "pc_time_end_measurement"]).dt.tz_localize(None)
        all_daytime_times = all_daytime_timestamps.dt.time
        first_time = np.min(all_daytime_times)
        last_time = np.max(all_daytime_times)
        spec_day.first_time, spec_day.last_time = first_time, last_time
        
        all_dates = all_daytime_timestamps.dt.date
        days = np.unique(all_dates)
        for day in days:
            day_data = data[data["pc_time_end_measurement"].dt.date == day]
            
            fig = plt.figure(figsize=(11.7, 8.3))
            axes = fig.subplots(4)
            
            spec_day.fig = fig
            spec_day.plot_all(day_data, axes)
            
            this_title = title + "Spectral data on "+day.strftime("%Y-%m-%d")
            fig.suptitle(this_title)
            
            spec_day.supplementary_integral_plot(day_data, axes, first_time, last_time, day, spec_day, True)
            
            plt.tight_layout()
            
            if self.output_location is not None:
                full_title = graphUtils.make_full_title(this_title)
                plt.savefig(self.output_location+"/spectrum_day_"+str(day)+".png")
            plt.show(block=self.block)
    
    
    def plot_dips_summary(self, n:int=15, cutoff_angle:float=np.radians(80), 
                          cutoff_wavelength:float=1000, 
                          reference_lines:list=None, 
                          reference_labels:list=None,
                          title="", dataframe=None):
        """histogram of the largest dips over a dataset
        params:
            n: the number of peaks that will be selected per measurement
            cutoff_angle: the maximum zenith angle included, used for excluding nighttime
            cutoff_wavelength: the maximum wavelength included
            reference_lines: list of wavelengths where dip should appear, 
                there is a default with the most prominent dips, 
                but you can provide your own if you want
            reference_labels: list of labels for the passed reference lines.
                must be the the same length as reference_lines, use ""
                if you dont want to label them all
            title: the title of the plot
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "global_spectrum"]
        """
        print("plotting dips summary")
        
        columns = ["pc_time_end_measurement", "global_spectrum", "sza"]
        data = self.load_data(columns, dataframe)
        
        data = data[data["sza"] < cutoff_angle]
        
        dailyDipsSummary = DailyDipsSummary(self.timezone, reference_lines, reference_labels)
        fig = dailyDipsSummary.plot_daily_peaks_summary(data, n, cutoff_wavelength)
        
        deployment_metadata = None
        if self.deployment_metadata is None and self.driver is not None:
            deployment_metadata = self.driver.load_metadata()
        else:
            deployment_metadata = self.deployment_metadata
        
        if title == "" and deployment_metadata is not None:
            title = deployment_metadata["deployment_description"][0]
        
        fig.suptitle(title+"\n", x=0.47)
        
        if deployment_metadata is not None:
            metadata_string = graphUtils.generate_metadata_string(deployment_metadata, data)
            plt.figtext(x=0.47, y=0.93, s=metadata_string, horizontalalignment="center")
        
        print("dips summary plotted")
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/dips_summary.png")
        
        
    
    
    def plot_integral(self, flag=False, title="", max_integral=None, dataframe=None):
        """plots a summary of the integral data in a dataset
        
        params:
            flag: when True, checks the data against the BSRN limits, and overlays
                the implausible readings in pink. 
            title: the title for the plot
            max_integral: the upper limit when plotting integral values, on
                the y-axes and on colourmaps.
                if None, selects the largest value in global or dni.
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "global_integral", "diffuse_integral", 
                 "gps_latitude", "gps_longitude", "gps_altitude", 
                 "sza", "azimuth", "toa_hi", "sed"]
        """
        
        print("plotting summary")
        
        
        time_day_graph = TimeDayGraph(self.jet_black_zero, diffuse_name=self.diffuse_name)
        elv_azimuth_graph = ElvAziGraph(diffuse_name=self.diffuse_name)
        clearness_graph = ClearnessDensityGraph(diffuse_name=self.diffuse_name)
        linear_graph = LinearTimeGraph(diffuse_name=self.diffuse_name)
        
        graphs = [time_day_graph, elv_azimuth_graph, clearness_graph, linear_graph]
        
        # time_day_graph.timezone = self.timezone
        
        
        requirements = ["gps_latitude", "gps_longitude", "gps_altitude"]
        for x in graphs:
            new_requirements = x.requirements["all"].copy()
            
            ##### this value will be calculated from other values, so is not in the database
            not_in_db_reqs = ["direct_normal_integral"]
            for not_in_db_req in not_in_db_reqs:
                if not_in_db_req in new_requirements:
                    new_requirements.remove(not_in_db_req)
            requirements += new_requirements
        
        data = self.load_data(requirements, dataframe)
        
        data = data.drop_duplicates(["pc_time_end_measurement"])
        
        if "gps_longitude" in requirements and not "gps_longitude" in data.columns:
            deployment_metadata = self.driver.db_load.load_metadata(["default_longitude", "default_latitude", "default_elevation"]).iloc[0]
            data["gps_longitude"] = deployment_metadata["default_longitude"]
            data["gps_latitude"] = deployment_metadata["default_latitude"]
            data["gps_altitude"] = deployment_metadata["default_elevation"]
        
        
        
        ##### filling in columns that arent in the database
        data["direct_normal_integral"] = ((data["global_integral"]-data["diffuse_integral"])/np.cos(data["sza"]))
        
        deployment_metadata = None
        if self.deployment_metadata is None and self.driver is not None:
            deployment_metadata = self.driver.db_load.load_metadata()
        else:
            deployment_metadata = self.deployment_metadata
        
        if max_integral is None:
            ##### calculating the maximum integral, will be shared across all graphs
            max_global_integral = max(data["global_integral"])
            max_normal_integral = np.max(data.loc[np.degrees(data["sza"]) < 80, "direct_normal_integral"])
            max_integral = max(max_global_integral, max_normal_integral)
            
            # max_integral = max(data["global_integral"])
            
            ##### adding 10% padding to the top
            max_integral = (int((max_integral+10)/100)+1)*100
                           
        for graph in graphs:
            graph.max_integral = max_integral
        
        flags = None
        if flag:
            flags = flagData.flag(data, ignore_nights=True)
        
        
        
        ##### make the subplot that the graphs will be plotted onto
        layout = [["ghi_time_day",  "ghi_elv_azi",  "ghi_elv_azi"],
                  ["diff_time_day", "diff_elv_azi", "diff_elv_azi"],
                  ["dni_time_day",  "dni_elv_azi",  "dni_elv_azi"],
                  ["ghi_linear",    "ghi_toa",      "sza_diff_ghi"],
                  ["diff_linear",   "diff_toa",     "ghi_dni_clearness"],
                  ["dni_linear",    "dni_toa",      "ghi_diff_clearness"]]
        
        
        ##### if the height and weight ratios are off, add 1s to the end to stop error
        gridspec_kw = {"height_ratios":(1,), "width_ratios":(3, 1, 1)}
        if len(gridspec_kw["height_ratios"]) < len(layout):
            gridspec_kw["height_ratios"] = tuple(list(gridspec_kw["height_ratios"]) + [1]* (len(layout) - len(gridspec_kw["height_ratios"])))
        
        if len(gridspec_kw["width_ratios"]) < len(layout[0]):
            gridspec_kw["width_ratios"] = tuple(list(gridspec_kw["width_ratios"]) + [1]* (len(layout[0]) - len(gridspec_kw["width_ratios"])))
        
        
        fig = plt.figure("integral", layout="constrained", figsize=(11.7, 8.3))
        axes = fig.subplot_mosaic(layout, gridspec_kw=gridspec_kw, )
        
        if title == "" and deployment_metadata is not None:
            title = deployment_metadata["deployment_description"][0]
        fig.suptitle(title+"\n")
        
        if deployment_metadata is not None:
            metadata_string = graphUtils.generate_metadata_string(deployment_metadata, data)
            plt.figtext(x=0.5, y=0.93, s=metadata_string, horizontalalignment="center")
        
        try:
            integral_axes = [axes["ghi_time_day"], axes["diff_time_day"], axes["dni_time_day"]]
            time_day_graph.graph_all(integral_axes, data[time_day_graph.requirements["all"]], fig, show_cbar=False, flags=flags, timedelta=self.timedelta)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to graph time/day summary\n"+str(e))
        
        
        try:
            linear_integral_axes = [axes["ghi_linear"], axes["diff_linear"], axes["dni_linear"]]
            linear_graph.graph_all(linear_integral_axes, data[linear_graph.requirements["all"]], flags=flags)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to graph linear integral summary\n"+str(e))
        
        try:
            elv_azimuth_axes = [axes["ghi_elv_azi"], axes["diff_elv_azi"], axes["dni_elv_azi"]]
            elv_azimuth_graph.graph_all(elv_azimuth_axes, data[elv_azimuth_graph.requirements["all"]], fig, flags=flags, show_horizon=False)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to graph elevation/azimuth summary\n"+str(e))
        
        flags = flagData.flag(data, ignore_nights=True)
        
        try:
            clearness_axes = [axes["ghi_toa"], axes["diff_toa"], axes["dni_toa"], axes["sza_diff_ghi"], axes["ghi_dni_clearness"], axes["ghi_diff_clearness"]]
            clearness_graph.graph_all(clearness_axes, data[clearness_graph.requirements["all"]], fig, flags=flags, flag_all=False, match_density=True)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to graph clearness summary\n"+str(e))
        
        
        print("summary plotted")
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/integral_summary.png")
        plt.show(block=self.block)
        
        
        
    
    def plot_accessory(self, title="", dataframe=None, accessory_dataframe=None):
        """generates a page of plots summarising the data in accessory_data
        contains:
            pressure, humidity and a comparison of the different temperature measurements
            voltage summary
            current summary
        
        params:
            title: the title of the plot
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "camera_temp"]
            accessory_dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "StatusFlags", "RH", "Pressure", "T_Bezel", 
                "T_Baro", "_15Vin", "Vcc", "I_Tot", "I_15VPC", "I_15VCAM","Latitude", "Longitude"]
        """
        
        print("plotting accessory_data")
        
        spectral_data = None
        
        ##### all the data that will be loaded from the accessory table of the database
        requirements = ["pc_time_end_measurement", 
                        "StatusFlags",
                        "RH", 
                        "Pressure", 
                        "T_Bezel", 
                        "T_Baro", 
                        "_15Vin", 
                        "Vcc", 
                        "I_Tot", 
                        "I_15VPC", 
                        "I_15VCAM",
                        "Latitude",
                        "Longitude"]
        
        data = self.load_data(requirements, accessory_dataframe)
        data = data.loc[data["StatusFlags"] != 0.0]
        
        spectral_requirements = ["pc_time_end_measurement", "camera_temp"]
        
        has_spectral_data = False
        try:
            spectral_data = self.load_data(spectral_requirements, dataframe)
            has_spectral_data = True
        except (ValueError, KeyError):
            print("spectral data could not be loaded or was not passed")
        
        
        
        layout = [["rh", "15vin"],
                  ["pressure", "vcc"],
                  ["tbezel", "itot"],
                  ["tbaro", "i15v"],
                  ["tcam", "icam"]]
        
        fig = plt.figure("accessory", layout="constrained", figsize=(11.7, 8.3))
        axes = fig.subplot_mosaic(layout)
        
        
        dh = DailyHists(data.copy(), fig)
        
        spectral_dh = None
        if has_spectral_data:
            spectral_dh = DailyHists(spectral_data, fig)
        
        try:
            dh.plot_one_hist("RH", axes["rh"], ignore_zero=True, show_xticks=False)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to plot relative humidity\n"+str(e))
        try:
            dh.plot_one_hist("Pressure", axes["pressure"], ignore_zero=True, show_xticks=False)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to plot presure\n"+str(e))
        
        ##### temps should have identical y-axes, so they are easier to compare,
        #####   this selects the largest and smallest values from any temp sensor to use as limits
        non_zero_temps = data.loc[np.logical_and((data["T_Baro"] != 0.0), (data["T_Bezel"] != 0.0))]
        accessory_min = 0
        accessory_max = 0
        if len(non_zero_temps) != 0:
            accessory_min = np.min(non_zero_temps[["T_Baro", "T_Bezel"]].to_numpy())
            accessory_max = np.max(non_zero_temps[["T_Baro", "T_Bezel"]].to_numpy())
        
        temp_ymin, temp_ymax = None, None
        
        if has_spectral_data:
            cam_min = min(spectral_data["camera_temp"])
            cam_max = max(spectral_data["camera_temp"])
            temp_ymin = min(accessory_min, cam_min)
            temp_ymax = max(accessory_max, cam_max)
        else:
            temp_ymin = accessory_min
            temp_ymax = accessory_max
        
        ten_percent = abs(temp_ymax-temp_ymin)*0.1
        temp_ymax += ten_percent
        temp_ymin -= ten_percent
        
        ##### plots the temperatures, with the calculated limits
        try:
            dh.plot_one_hist("T_Bezel", axes["tbezel"], ignore_zero=True, ylims=(temp_ymin, temp_ymax), show_xticks=False)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to plot bezel temp\n"+str(e))
        try:
            dh.plot_one_hist("T_Baro", axes["tbaro"], ignore_zero=True, ylims=(temp_ymin, temp_ymax), show_xticks=False)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to plot barometer temp\n"+str(e))
        if has_spectral_data:
            try:
                spectral_dh.plot_one_hist("camera_temp", axes["tcam"], ignore_zero=True, ylims=(temp_ymin, temp_ymax))
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("failed to plot camera temp\n"+str(e))
        
        ##### plots the voltages
        try:
            dh.plot_one_hist("_15Vin", axes["15vin"], ignore_zero=True, show_xticks=False)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to plot 15Vin\n"+str(e))
        try:
            dh.plot_one_hist("Vcc", axes["vcc"], ignore_zero=True, show_xticks=False)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to plot Vcc\n"+str(e))
        
        ##### calculates the limits for the shared current axes(see comment above temps)
        non_zero_temps = data.loc[np.logical_and((data["I_Tot"] != 0.0), (data["I_15VPC"] != 0.0))]
        current_ymin = np.min(non_zero_temps[["I_Tot", "I_15VPC"]].to_numpy())
        current_ymax = np.max(non_zero_temps[["I_Tot", "I_15VPC"]].to_numpy())*1.1
        
        ##### plots the currents
        try:
            dh.plot_one_hist("I_Tot", axes["itot"], ignore_zero=True, zero_axes=True, ylims=(current_ymin, current_ymax), show_xticks=False)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to plot I_Tot\n"+str(e))
        try:
            dh.plot_one_hist("I_15VPC", axes["i15v"], ignore_zero=True, zero_axes=True, ylims=(current_ymin, current_ymax), show_xticks=False)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to plot I_15VPC\n"+str(e))
        try:
            dh.plot_one_hist("I_15VCAM", axes["icam"], ignore_zero=False, zero_axes=True)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print("failed to plot I_15VCAM\n"+str(e))
        
        ##### uses the passed value of deployment metadata as a default, 
        deployment_metadata = self.deployment_metadata
        if deployment_metadata is None and self.driver is not None:
            ##### loads everything from the deployment metadata and generates the title and description
            deployment_metadata = self.driver.db_load.load_metadata()
        
        if deployment_metadata is None:
            print("No Deployment metadata available for the title")
        else:
            if title == "":
                title = deployment_metadata["deployment_description"][0]
            fig.suptitle(title+"\n")
            metadata_string = graphUtils.generate_metadata_string(deployment_metadata, data)
            plt.figtext(x=0.5, y=0.93, s=metadata_string, horizontalalignment="center")
        
        print("accessory_data plotted")
        if self.output_location is not None:
            plt.savefig(self.output_location+"/accessory_summary.png")
        plt.show(block=self.block)
        

    def plot_gps(self, title="", dataframe=None, accessory_dataframe=None):
        """plots a summary of gps related data
        contains:
            plots of gps position thougout the dataset, with the colour representing the time and reading density
            a plot of the difference between pc time and gps time. log scale with linear segment
            a plot of gps age. log scale with linear segment
            plot of number of satelites in view
            plot of tilt: sqrt(pitch^2*roll^2)
        
        params:
            title: the title of the plot
            dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "camera_temp"]
            accessory_dataframe: to plot the graph from an already generated dataset, 
                pass it here, dataframe must have columns:
                ["pc_time_end_measurement", "StatusFlags", "RH", "Pressure", "T_Bezel", 
                "T_Baro", "_15Vin", "Vcc", "I_Tot", "I_15VPC", "I_15VCAM","Latitude", "Longitude"]
        """
        print("plotting GPS")
        ##### loading data from the database or from the provided dataframes
        ##### accessory_data will be used if available but if not, system_data will be used
        data = None
        gps_type = ""
        try:
            accessory_requirements = ["pc_time_end_measurement",
                                      "StatusFlags",
                                      "gps_time", 
                                      "GPSAge",
                                      "NSV",
                                      "Roll", "Pitch",
                                      "Latitude", "Longitude"]
            data = self.load_data(accessory_requirements, accessory_dataframe)
            gps_type = "accessory"
        except (ValueError, KeyError):
            try:
                requirements = ["pc_time_end_measurement",
                                "gps_longitude",
                                "gps_latitude",
                                "gps_time",
                                "gps_status",
                                "baro_temp",
                                "pressure",
                                "rh"]
                data = self.load_data(requirements, dataframe)
                gps_type = "GPS"
            except (ValueError, KeyError):
                raise ValueError("insufficient columns to plot gps")
        
        
        layout = [["gps_density", "time_diff"],
                  ["gps_density", "gps_age"],
                  ["gps_time", "NSV"],
                  ["gps_time", "tilt"]]
        fig = plt.figure("gps", layout="constrained", figsize=(11.7, 8.3))
        axes = fig.subplot_mosaic(layout)
        
        
        
        data = data.copy()
        
        ##### ignore all the data where StatusFlags is 0
        #####   this filters out all the rows where all the data is 0
        if gps_type == "accessory":
            data = data.loc[data["StatusFlags"] != 0.0]
        else:
            data = data.loc[~data["gps_time"].isnull()]
            data = data.loc[data["gps_longitude"] != ""]
            data[["gps_longitude", "gps_latitude"]] = data[["gps_longitude", "gps_latitude"]].astype(float)
        
        
        ##### locations where gps_time is 0
        zero_times = data["gps_time"].str.slice(0, 1) == "0"
        
        gps_times = data["gps_time"].copy()
        gps_times[zero_times] = np.nan
        ##### converts gps_time and pc time to an integer number of seconds
        gps_time_index = pd.DatetimeIndex(gps_times, dtype="datetime64[s]")
        gps_time_int = gps_time_index.to_numpy().astype(float)
        gps_time_int[zero_times] = np.nan
        
        pc_time_index = pd.DatetimeIndex(data["pc_time_end_measurement"].dt.tz_convert(None), dtype="datetime64[s]")
        pc_time_int = pc_time_index.to_numpy().astype(float)
        pc_time_int[zero_times] = np.nan
        
        data["gps time - pc time"] = (gps_time_index-pc_time_index).total_seconds()
        
        
        if gps_type == "accessory":
            ##### tilt is the angle that the instrument is away from level
            data["tilt"] = np.sqrt(np.power(data["Roll"], 2)+np.power(data["Pitch"], 2))
        
        ##### plots the histograms
        dh = DailyHists(data.copy())
        try:
            dh.plot_one_hist("gps time - pc time", axes["time_diff"], ignore_zero=False, weight=True, ybuffer=False, log=True, linthresh=10, lin_ticks=3, log_ticks_skipped=0)#, ylims=[-10**10, 10**4])
        except Exception as e:
            print("failed plotting gps_time - pc_time comparison\n"+str(e))
        
        if gps_type == "accessory":
            try:
                dh.plot_one_hist("GPSAge", axes["gps_age"], log=True, ybuffer=True)
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("failed plotting GPSAge\n"+str(e))
            try:
                dh.plot_one_hist("NSV", axes["NSV"], limited_bins=True, zero_axes=True)
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("failed plotting NSV\n"+str(e))
            try:
                dh.plot_one_hist("tilt", axes["tilt"])
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("failed plotting tilt\n"+str(e))
        elif gps_type == "GPS":
            try:
                dh.plot_one_hist("baro_temp", axes["gps_age"])
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("failed plotting baro_temp\n"+str(e))
            try:
                dh.plot_one_hist("pressure", axes["NSV"])
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("failed plotting pressure\n"+str(e))
            try:
                dh.plot_one_hist("rh", axes["tilt"])
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("failed plotting tilt\n"+str(e))
        
        lat_lon_name = ["Latitude", "Longitude"]
        if gps_type == "GPS":
            lat_lon_name = ["gps_latitude", "gps_longitude"]
            
            
        ##### plots the gps graphs
        ll = LatLonGraph(data)
        try:
            density_im = ll.plot_lat_lon(axes["gps_density"], stack_resolution="max", lat_lon_name=lat_lon_name)
            cbar = fig.colorbar(density_im, ax=axes["gps_density"], format='%.0f')
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            print("failed plotting gps frequency")
        try:
            time_im = ll.plot_lat_lon(axes["gps_time"], "pc_time_end_measurement", stack_resolution="max", lat_lon_name=lat_lon_name)
            cbar = fig.colorbar(time_im, ax=axes["gps_time"])
            
            ##### generates the ticks and converts to string date format
            ticks = np.linspace(cbar.vmin, cbar.vmax, 5)
            labels = [datetime.fromtimestamp(int(tick/10**9)).strftime("%Y-%m-%d") for tick in ticks]
            cbar.ax.set_yticks(ticks, labels)
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            print("failed plotting gps time")
        
        
        
        deployment_metadata = self.deployment_metadata
        if deployment_metadata is None:
            if self.driver is not None:
                deployment_metadata = self.driver.db_load.load_metadata()
        
        if title == "" and deployment_metadata is not None:
            title = deployment_metadata["deployment_description"][0]
        fig.suptitle(title+"\n")
        
        if deployment_metadata is not None:
            metadata_string = graphUtils.generate_metadata_string(deployment_metadata, data)
            plt.figtext(x=0.5, y=0.93, s=metadata_string, horizontalalignment="center")
    
        print("GPS plotted")
        if self.output_location is not None:
            plt.savefig(self.output_location+"/GPS_summary.png")
        plt.show(block=self.block)
    
    
    def __make_colormap(self):
        """makes a new colormap which is jet but a value of 0 is black rather than white
        returns: new colormap
        """
        black = np.array([0,0,0,1])
        
        jet = None
        ##### accounting for different matplotlib versions
        mpl_version = matplotlib.__version__
        mpl_version = mpl_version.split(".")
        if int(mpl_version[0]) > 3 or (int(mpl_version[0]) == 3 and int(mpl_version[1]) > 5):
            jet = matplotlib.colormaps["jet"].resampled(256)
        else:
            jet = matplotlib.colormaps["jet"]._resample(256)
            
        new_colors = jet(np.linspace(0, 1, 256))
        new_colors[0] = black
        new_cmap = matplotlib.colors.ListedColormap(new_colors)
        return new_cmap
    
    
    def load_spectrum(self, cutoff_angle, **kwargs):
        """loads the global spectrum from the database, taking into account cutoff angle
        params:
            cutoff_angle: None | float(radians) | tuple[float](radians)
                          the angle(s) range to include
        returns:
            spectrum: the requested spectrum, and time
        """
        spectrum = []
        if cutoff_angle is None:
            spectrum = self.driver.db_load.load(["pc_time_end_measurement", "global_spectrum"])
        elif type(cutoff_angle) == type((0, )):
            if len(cutoff_angle) == 2:
                condition="sza < "+str(cutoff_angle[1]) + " AND sza > "+str(cutoff_angle[0])
                spectrum = self.driver.db_load.load(["pc_time_end_measurement", "global_spectrum"], 
                                                    condition=condition, 
                                                    **kwargs)
            else:
                spectrum = self.driver.db_load.load(["pc_time_end_measurement", "global_spectrum"], 
                                                    **kwargs)
        else:
            spectrum = self.driver.db_load.load(["pc_time_end_measurement", "global_spectrum"], 
                                                condition="sza < "+str(cutoff_angle), 
                                                **kwargs)
        
        if len(spectrum) == 0:
            raise Exception("could not load spectrum")
        
        return spectrum
    
    def load_data(self, columns, dataframe):
        """returns a dataframe with the requested columns. either from the passed dataframe
        or from the dbdriver if that is missing.
        """
        columns = np.array(columns + ["pc_time_end_measurement"])
        if dataframe is not None:
            if np.isin(columns, dataframe.columns).all():
                return dataframe.copy()
        
        if self.driver is None:
            raise ValueError("database is None and not all the required columns were passed to dataframe")
        
        return self.driver.load(columns, **self.kwargs)
                
            
        
    
    def wait_until_closed(self):
        """stops matplotlib from closing all the plots when the last one is generated
        only relevant when block=False in Graph.
        """
        plt.show()

