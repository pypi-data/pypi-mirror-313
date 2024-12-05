# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import hsr_spectrum.spectrumUtils as SpectrumUtils
from hsr1.utils.spectrum import spectrumUtils as SpectrumUtils

class PixelSpectrum:
    def __init__(self, cal_poly=None, poly_list=None):
        ##### calibration: contains the polynomial used for wavelength calibration, read from file
        self.cal_poly = cal_poly
        self.poly_list = poly_list
    
    def calculate_from_wavelengths(self, wavelength_spectra:[pd.DataFrame], data_cols):
        spectra = wavelength_spectra.copy()
        old_spectra = wavelength_spectra.copy()
        for i, channel in enumerate(data_cols):
            poly = self.cal_poly
            if self.poly_list is not None:
                poly = self.poly_list[i]
            sample_pixels = np.arange(0, 1200)
            sample_wavelengths = np.array([SpectrumUtils.apply_polynomial(pixel, poly[0], poly[1], poly[2], poly[3]) for pixel in sample_pixels])
            
            for j in range(len(spectra)):
                indecies = np.arange(300, 1101)
                spectra.loc[j, channel] = self.apply_wavelength_calibration(spectra.loc[j, channel], poly, indecies, flip=True)
                
        spectra["pc_time_end_measurement"] = old_spectra["pc_time_end_measurement"]
        return spectra



    def apply_wavelength_calibration(self, spectrum, poly, indecies=np.arange(1200), inverse=False, flip=None, output_shape=None, isdf=None, plot=False): 
        """takes a polynomial and shifts the spectrum according to that polynomial
        params:
            spectrum: the spectrum being converted
            poly: the polynomial calibration
            indecies: the size of the input array
            inverse: wether the polynomial is applied or is inverse, wavelength->pixel = True
            flip: some usecases require both inputs to be flipped so they are ascending, 
                    usually flip=True when applying inverse, and vice versa but there are some situations where this isnt the case
            output shape: [start, stop]the cropping to apply once calibrated
        
        to apply a pixel -> wavelength calibration, inverse=True and default values should work
        to apply a wavelength -> pixel calibration, use the constructor and calculate_from_wavelength
        to apply a wavelength -> wavelength calibration in index space, indecies should be np.arange(801) and output shape should be [0, 801]
        to apply a wavelength -> wavelength calibration in wavelength space, indecies should be np.arange(300, 1001) and output shape should be [300, 1101]
        
        """
        if output_shape is None:
            if inverse:
                output_shape = (300, 1101)
            else:
                output_shape = (0, 1200)
        
        if isdf is None:
            if isinstance(spectrum, pd.DataFrame):
                isdf = True
            else:
                isdf = False
        
        if isdf:
            ##### df of spectra
            spectrum = spectrum.copy()
            
            for i in range(len(spectrum)):
                one_spectrum = spectrum["global_spectrum"].iloc[i]
                if inverse:
                    if flip is None:
                        flip=True
                    corresponding_pixels = SpectrumUtils.apply_inverse_polynomial(indecies, poly[0], poly[1], poly[2], poly[3])
                else:
                    if flip is None:
                        flip=False
                    corresponding_pixels = SpectrumUtils.apply_polynomial(indecies, poly[0], poly[1], poly[2], poly[3])
                
                if flip:
                    corresponding_pixels = np.flip(corresponding_pixels)
                    one_spectrum = np.flip(one_spectrum)
                
                result = np.interp(np.arange(-1200, 2400), corresponding_pixels, one_spectrum)    
                output_shape = [output_shape[0]+1200, output_shape[1]+1200]
                spectrum.loc[i, "global_spectrum"] = result[output_shape[0]:output_shape[1]]
            return spectrum
        
        else:
            ##### single spectrum
            if inverse:
                if flip is None:
                    flip=True
                corresponding_pixels = SpectrumUtils.apply_inverse_polynomial(indecies, poly[0], poly[1], poly[2], poly[3])
            else:
                if flip is None:
                    flip=False
                corresponding_pixels = SpectrumUtils.apply_polynomial(indecies, poly[0], poly[1], poly[2], poly[3])
            
            if flip:
                corresponding_pixels = np.flip(corresponding_pixels)
                spectrum = np.flip(spectrum)
            
            
            result = np.interp(np.arange(-1200, 2400), corresponding_pixels, spectrum)
            
            if plot:
                plt.plot(indecies)
                plt.show(block=False)
                plt.plot(corresponding_pixels)
                plt.show(block=False)
                plt.plot(spectrum)
                plt.plot(result)
                plt.show(block=False)
            
            output_shape = [output_shape[0]+1200, output_shape[1]+1200]
            return result[output_shape[0]:output_shape[1]]
    
    
    def apply_constant_wavelength_calibration(self, spectrum, cal):
        """applied a constant shift left or right
        params:
            spectrum: the spectrum to be shifted
            cal: the amount to shift by
        returns:
            spectrum: shifted spectrum
        
        pads with zeros
        """
        cal = int(cal)
        if cal == 0:
            return spectrum
        if cal >= 0:
            spectrum = np.concatenate(([0]*cal,  spectrum[:-cal]))
        else:
            spectrum = np.concatenate((spectrum[-cal:], [0]*-cal))
        
        return spectrum
    
    
    def apply_origin_wavelength_calibration(self, spectrum, poly, origin):
        """applies a calibration to a spectrum around a specific wavelength
        params:
            spectrum: the spectrum to be calibrated
            poly: the polynomial being applied
            origin: the point around which the poynomial is being applied
        returns:
            calibrated: calibrated spectrum
        """
        left=spectrum[:origin]
        origin_value = np.array([spectrum[origin]])
        right = spectrum[origin+1:]
        
        ##### calibrates the spectrum to the left and right of the origin and adds the 3 together
        left_pos = int(SpectrumUtils.apply_polynomial(len(left), poly[0], poly[1], poly[2], poly[3]))
        cal_left = []
        if len(left) > 0:
            cal_left = self.apply_wavelength_calibration(left, poly, np.arange(len(left)), output_shape=[left_pos-len(left), left_pos], isdf=False)
        
        cal_right = []
        if len(right) > 0:
            cal_right = self.apply_wavelength_calibration(right, poly, np.arange(len(right)), output_shape=[0, len(right)], isdf=False)
        
        calibrated = np.concatenate((cal_left, origin_value, cal_right))
        return calibrated
    

    def apply_amplitude_calibration(self, spectrum, calibration):
        return spectrum*calibration