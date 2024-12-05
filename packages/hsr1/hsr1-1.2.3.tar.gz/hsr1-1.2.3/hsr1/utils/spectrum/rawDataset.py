# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import importlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from hsr1.utils.spectrum import spectrumUtils as SpectrumUtils
from hsr1.utils.spectrum.pixelSpectrum import PixelSpectrum
from hsr1.utils.spectrum.weightedSpectrum import WeightedSpectrum


class RawDataset:
    def __init__(self, dataset:pd.DataFrame, 
                 calibrations:dict=None, calibrations_filepath=None, 
                 amplitude_calibration=None, amplitude_calibration_filepath=None, 
                 spectrum_type="wavelength"):
        """stores a raw dataset containing all the channels of raw data
        
        params:
            dataset: dataframe with columns "pc_time_end_measurement", "channel_0", "channel_1" etc.
            calibrations: dict containing polynomials with keys "channel_0", "channel_1" etc.
            calibrations_filepath: filepath to the current wavelength calibration file
            amplitude_cal: an amplitude calibration to apply to found spectrum, only used for graphs
            amplitude_calibration_filepath
        """
        self.dataset = dataset
        self.calibrations = calibrations
        self.amplitude_calibration = amplitude_calibration
        self.spectrum_type = spectrum_type
        
        if spectrum_type != "wavelength" and spectrum_type != "pixel":
            raise ValueError("spectrum_type must be either \"wavelength\" or \"pixel\"")
        
        if calibrations is None and spectrum_type == "wavelength":
            if calibrations_filepath is None:
                raise ValueError("""original calibrations must be passed, either as a dict or as the location of the calibration file. If this is uncalibrated data, pass spectrum_type=\"pixel\"""")
            self.calibrations = SpectrumUtils.read_wavelength_polys(calibrations_filepath)
        
        if spectrum_type == "pixel":
            if calibrations is not None or calibrations_filepath is not None:
                print("there is no point passing existing calibrations to a pixel dataset, pixel readings are assumed to be uncalibrated. \
                      \n if this is a calibration that is used on this spectrometer, you can change the default_calibration parameter in find_all_calibrations.")
        
        if amplitude_calibration is None and amplitude_calibration_filepath is not None:
            self.amplitude_calibration = SpectrumUtils.read_amplitude_file(amplitude_calibration_filepath)
        
        if amplitude_calibration is None and amplitude_calibration_filepath is None:
            self.amplitude_calibration = np.ones(801)
        
    
    
    def plot_calibration(self, polys, names=None):
        """plots a line graph of pixel against wavelength for each channel
        params:
            polys: list of lists or dict containing the polynommials for each channel's new calibration
            names: list of names to display on the legend
        """
        ps = PixelSpectrum()
        
        
        if isinstance(polys, dict):
            poly_names = []
            poly_list = []
            for poly in polys:
                poly_list.append(polys[poly])
                poly_names.append(poly)
            polys = poly_list 
            names = poly_names
        
        if names is None:
            names = [""]*len(polys)
        
        plt.figure(figsize=(20,10))
        for poly, name in zip(polys, names):
            plt.plot(ps.apply_wavelength_calibration(np.arange(0, 1200), poly, inverse=True), np.arange(300, 1101), linewidth=0.5, label=name + ": "+SpectrumUtils.poly_to_string(poly))
        plt.xlim(0, 1200)
        plt.suptitle("individual channel calibrations")
        plt.xlabel("pixels")
        plt.ylabel("wavelength")
        plt.legend()
        plt.show(block=False)
    
    def plot_calibration_wide(self, polys, names=None, title=""):
        """plots a line graph of pixel against wavelength for each channel
        params:
            polys: list of lists containing the polynommials for each channel's new calibration
            names: list of names to display on the legend
        """
        if names is None:
            names = [""]*len(polys)
        
        plt.figure(figsize=(20,10))
        for poly, name in zip(polys, names):
            x = np.linspace(-10000, 10000, 1000)
            y = [SpectrumUtils.apply_polynomial(i, poly[0], poly[1], poly[2], poly[3]) for i in x]
            plt.plot(x, y, label=name + ": " + SpectrumUtils.poly_to_string(poly))

        plt.axvline(0)
        plt.axvline(1200)
        plt.suptitle(title)
        plt.legend()
        plt.show(block=False)
    
    def plot_all_errors(self, polys, dips, names):
        plt.figure(figsize=(20, 10))
        for i, poly, _dips, name in zip(list(range(len(polys))), polys, dips, names):
            measured = _dips[0]
            ref = _dips[1]
            error = measured-ref
            
            plt.plot(ref, error-(i/50), label=name)
        
        plt.legend()
        plt.show(block=False)
    
    
    def find_all_calibrations(self, file_output=None, 
                              reference_spectrum=None, reference_filepath=None, 
                              plot_total_output=True, plot_individual_results=False, plot_debug=False, 
                              **kwargs):
        """loops through each channel in the dataset and finds the correct calibration
        params:
            file_output: for outputting results, which text file to use. leave as None to not output
            reference_spectrum: a spectrum in wavelength space that the measured data will be matched to
            plot_total_output: plots the calibration for each channel on one graph
            plot_individual_results: plots the results from each channel, passes plot_results to each calibration
            plot_debug: plots the result from each segment of each channel, passed to each calibration
            kwargs: arguments to pass to each channel's find_calibration method, cleaner than having all arguments as parameters here
        """
        if reference_filepath is None:
            res = importlib.resources.files("hsr1.data").joinpath("smarts.txt")
            file = importlib.resources.as_file(res)
            with file as f:
                reference_filepath = f
            
        
        
        if reference_spectrum is None:
            try:
                reference_spectrum = SpectrumUtils.read_simple_file(reference_filepath)
            except ValueError:
                reference_spectrum = SpectrumUtils.read_reference_file(reference_filepath)
        
        
        all_dips = []
        polys = []
        names = []
        new_calibrations = {}
        for channel_name in self.dataset.columns[1:]:
            
            
            ##### extract the polynomial that has already been applied to this channel
            applied_poly = None
            if self.spectrum_type == "wavelength":
                if channel_name in self.calibrations:
                    applied_poly = self.calibrations[channel_name]
                else:
                    print("error while calibrating "+channel_name+": couldnt find an existing calibration for this channel")
                    continue
            
            ps = PixelSpectrum(cal_poly=applied_poly)
            
            channel = self.dataset[["pc_time_end_measurement", channel_name]].copy()
            channel = channel.rename(columns={channel_name: "global_spectrum"})
            
            
            
            ##### calculate one pixel spectrum, for graphing
            pixel_spectrum = None
            if self.spectrum_type == "wavelength":
                pixel_data = ps.calculate_from_wavelengths(channel, ["global_spectrum"])
                max_index = 0
                if len(channel) > 1:
                    integrals = pixel_data["global_spectrum"].apply(np.sum)
                    max_index = np.argmax(integrals)
                pixel_spectrum = pixel_data.loc[max_index, "global_spectrum"]
            elif self.spectrum_type == "pixel":
                max_index = 0
                if len(channel) > 1:
                    integrals = channel.apply(np.sum)
                    max_index = np.argmax(integrals)
                pixel_spectrum = channel.loc[max_index, "global_spectrum"]
            
            if max(pixel_spectrum) == 0:
                print("invalid spectrum selected for graphing")
            
            ##### calculate the weighted spectrum and calibrate
            ws = None
            if self.spectrum_type == "wavelength":
                ws = WeightedSpectrum(wavelength_spectra=channel, reference_spectrum=reference_spectrum, 
                                      applied_poly=applied_poly, 
                                      filter_low_values=False, 
                                      amplitude_calibration=self.amplitude_calibration, 
                                      pixel_spectrum=pixel_spectrum, 
                                      name=channel_name, **kwargs)
            elif self.spectrum_type == "pixel":
                ws = WeightedSpectrum(pixel_spectra=channel, reference_spectrum=reference_spectrum, 
                                      applied_poly=applied_poly, 
                                      filter_low_values=False, 
                                      amplitude_calibration=self.amplitude_calibration, 
                                      pixel_spectrum=pixel_spectrum, 
                                      name=channel_name, **kwargs)
                
            wavelength_cal, dips = (None, None)
            if plot_total_output:
                wavelength_cal, dips = ws.find_calibration(plot_debug=plot_debug, plot_results=plot_individual_results, 
                                                            return_dips=plot_total_output, 
                                                            **kwargs)
            else:
                wavelength_cal = ws.find_calibration(plot_debug=plot_debug, plot_results=plot_individual_results, 
                                                            return_dips=plot_total_output, 
                                                            **kwargs)
            if wavelength_cal is not None:
                all_dips.append(dips)
                new_calibrations[channel_name] = wavelength_cal
                polys.append(wavelength_cal)
                names.append(channel_name)
        
        if plot_total_output:
            self.plot_calibration(polys, names)
            self.plot_calibration_wide(polys, names)
            self.plot_all_errors(polys, all_dips, names)
        
        if file_output is not None:
            SpectrumUtils.format_output(new_calibrations, file_output)
        
        return new_calibrations