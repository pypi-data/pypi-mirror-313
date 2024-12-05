# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import numpy as np
import matplotlib.pyplot as plt

from hsr1.utils.spectrum.pixelSpectrum import PixelSpectrum


class WeightedSpectrumSegment:
    def __init__(self, ref_spectrum, measured_spectrum, centre, distance, old_centre_point):
        self.ref_spectrum = ref_spectrum
        self.measured_spectrum = measured_spectrum
        
        self.distance = distance
        
        self.old_centre_point = old_centre_point
        
        self.left = centre-distance
        self.right = centre+distance
        
        left_padding_dist = max(0, self.left)
        right_padding_dist = max(0, len(ref_spectrum)-(self.right))
        
        error = 0
        if self.left <0:
            error = abs(self.left)
            self.left = 0
        
        self.segment = ref_spectrum[self.left:self.right]
        
        if error > 0:
            self.segment = np.concatenate((self.segment, np.zeros(error)))
            right_padding_dist -= error
        
        self.windowed_spectrum = np.concatenate((np.zeros(left_padding_dist), self.segment, np.zeros(right_padding_dist)))
        if max(self.windowed_spectrum) > 0:
            self.windowed_spectrum = self.windowed_spectrum/max(self.windowed_spectrum)
        
        self.centre = centre
        
    
    
    def plot(self, c0, c1, fit_quality, calibrated_spectrum):
        plt.figure(figsize=(20,10))
        plt.suptitle(str(c0) + "\n" + str(c1) + f"\n{fit_quality:.2e}")
        plt.plot(self.windowed_spectrum)
        plt.plot(calibrated_spectrum, label="calibrated")
        plt.axvline(self.centre, c="black")
        plt.axvline(self.centre+self.distance, c="gray")
        plt.axvline(self.centre-self.distance, c="gray")
        plt.legend()
        plt.show(block=False)
        
    
    def find_best_calibration(self, c0_init, c1_init, 
                              c0_lim, c1_lim,
                              iterations=20,
                              plot=False, debug=True):
        """finds the best calibration for this segment
        params:
            c0_init: the starting c0 value
            c1_init: the starting c1 value
            c0_lim: how far to the left and right to shift
            c1_lim: how much to stretch and squash by
            iterations: How many different stretch values to try within the limit (every integer shift is tried within the limits)
            plot: plot every single set of values and the calibrated spectrum they produce
            debug: return debug info
        returns:
            poly: polynomial calibration for this segment
            all_attempts: a 2d array of all the fit quality for all the tested values
        """
        ps = PixelSpectrum()
        
        ##### when a neighbouring segment squashes the spectrum, assuming it
        #####   has an accurate calibration for that segment, will be a good starting point for this segment.
        #####   not only can we start by using the c0 and c1 values from the previous segment,
        #####   but we can also apply a slight extra shift to account for this segment's
        #####   centre point being slightly off from where the previous segment's calibration would suggest it might be.
        #####   by applying a shift of previous_stretch-1 * change_in_centre_points,
        #####   we can get a more accurate guess of the starting shift, and can therefore have a more restricted c0_lim
        
        adjustment = (c1_init-1)*(self.centre-self.old_centre_point)
        c0_init += adjustment
        
        results = {}
        all_attempts = []
        ##### c1 is applied before c0, because a stretch takes longer than a shift so this reduces the total time
        for c1 in np.linspace(c1_init-c1_lim, c1_init+c1_lim, iterations):
            ##### apply the new c1
            stretched_spectrum = ps.apply_origin_wavelength_calibration(self.measured_spectrum, (0, c1, 0, 0), self.centre)
            shift_results = []
            for c0 in np.arange(c0_init-c0_lim, c0_init+c0_lim):
                ##### apply the shift
                calibrated_spectrum = ps.apply_constant_wavelength_calibration(stretched_spectrum, c0)
                
                if len(calibrated_spectrum[self.left:self.right]) > 0 and max(calibrated_spectrum[self.left:self.right]) > 0:
                    ##### normalise
                    calibrated_spectrum = calibrated_spectrum/max(calibrated_spectrum[self.left:self.right])
                
                
                ##### calculates fit_quality
                fit_quality = np.sum(calibrated_spectrum*self.windowed_spectrum)
                results[(c0, c1)] = fit_quality
                shift_results.append(fit_quality)
                
                if plot:
                    self.plot(c0, c1, fit_quality, calibrated_spectrum)
            
            all_attempts.append(np.array(shift_results))
        all_attempts = np.array(all_attempts)
        
        ##### pick the polynomial that has the best fit quality
        best_fit = max(results, key=results.get)
        
        if debug:
            return [best_fit[0], best_fit[1], 0, 0], all_attempts
        
        return [best_fit[0], best_fit[1], 0, 0]
                
    