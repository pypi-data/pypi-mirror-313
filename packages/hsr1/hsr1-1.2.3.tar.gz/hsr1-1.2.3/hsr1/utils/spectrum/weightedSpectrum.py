# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import lmfit

from hsr1.utils.spectrum.pixelSpectrum import PixelSpectrum
from hsr1.utils.spectrum.weightedSpectrumSegment import WeightedSpectrumSegment

import hsr1.utils.spectrum.spectrumUtils as SpectrumUtils


class WeightedSpectrum:
    def __init__(self, weighted_spectrum=None, wavelength_spectra=None, 
                 weighted_pixel_spectrum=None, pixel_spectra=None, 
                 weighted_reference=None, reference_spectrum=None, 
                 applied_poly=None, amplitude_calibration=None, 
                 default_poly=[1623, -1.4, 0, 0],
                 filter_low_values=False, num_reference_dips=30, 
                 pixel_spectrum=None, 
                 name="", find_peaks=False,
                 graph_limits=[300, 1101],
                 **kwargs):
        """represents the location and prominence of dips over the whole dataset
        params:
            weighted_spectrum: if you alredy have a weighted spectrum, you can just pass it in here
            wavelength_spectra: dataframe to be converted to a weighted spectrum
            weighted_pixel_spectrum: weighted spectrum in pixel space. 
                        will have a default calibration applied to it to convert into wavelength space, to compare with the reference
            pixel_spectra: dataframe containing pixel data, will be converted into a wavelength spectrum and then a weighted spectrum
            weighted_reference: weighted reference spectrum
            reference_spectrum: spectrum to be converted to weighted_reference
            lin_cal: for manually finding the first dip, input how much to move the measured spectrum by
                        (not usually needed but maybe helpful for very uncalibrated spectra)
            applied_poly: the polynomial that has already been applied to this spectrum
            filter_low_values: wether or not to filter out spectra with low total intensities,
                        as bright days will have clearer spectrums.
            pixel_spectrum: an example pixel spectrum, ideally taken from this dataset
                        not used for calculation, but helpful for plotting the calibration
            name: name to display on graphs
        """
        self.reference = reference_spectrum
        self.weighted_reference = weighted_reference
        self.wavelength_spectra = wavelength_spectra
        self.pixel_spectra = pixel_spectra
        
        if np.max(pixel_spectrum) == 0:
            print("channel " + name + " is all zeros")
        else:
            self.pixel_spectrum = pixel_spectrum/np.max(pixel_spectrum)
        
        self.applied_poly = applied_poly
        self.amplitude_calibration = amplitude_calibration
        
        self.ps = PixelSpectrum(0)
        
        self.default_poly = default_poly
        
        self.filter_low_values = filter_low_values
        self.find_peaks = find_peaks
        
        self.num_reference_dips = num_reference_dips
        
        self.spectrum, self.source = self.calculate_spectrum(weighted_spectrum, 
                                                             wavelength_spectra,
                                                             weighted_pixel_spectrum,
                                                             pixel_spectra)
        
        
        if self.amplitude_calibration is not None:
            self.spectrum = self.ps.apply_amplitude_calibration(self.spectrum, self.amplitude_calibration)
        
        if self.weighted_reference is None:
            self.weighted_reference = pd.DataFrame({"global_spectrum":[self.reference]})
            self.weighted_reference = self.generate_weighted_frequency(self.weighted_reference, n=num_reference_dips)
            
        self.reference_peaks = self.find_n_peaks(self.weighted_reference)
        
        
        
        self.calibration = None
        self.calibrated_spectrum = None
        
        self.poly_cal = None
        
        self.name = name
        self.graph_limits = graph_limits
    
    
    def calculate_spectrum(self, weighted_spectrum=None, wavelength_spectra=None, weighted_pixel_spectrum=None, pixel_spectra=None):
        """calculates the weighted spectrum given all the possible input types"""
        if weighted_spectrum is not None:
            return weighted_spectrum, "weighted_wavelength_spectrum"
        
        if weighted_pixel_spectrum is not None:
            return weighted_pixel_spectrum, "weighted_pixel_spectrum"
        
        if wavelength_spectra is not None:
            calc_weighted_spectrum = self.generate_weighted_frequency(wavelength_spectra, filter_low_values=self.filter_low_values)
            return calc_weighted_spectrum, "wavelength spectra"
        
        if pixel_spectra is not None:
            self.applied_poly = self.default_poly
            wavelength_spectra = self.ps.apply_wavelength_calibration(pixel_spectra, self.applied_poly, inverse=True)
            calc_weighted_spectrum = self.generate_weighted_frequency(wavelength_spectra, filter_low_values=self.filter_low_values) 
            return calc_weighted_spectrum, "pixel_spectra"
        
    
    def generate_weighted_frequency(self, global_spectrum=None, column_name="global_spectrum", cutoff_angle=np.radians(80), cutoff_wavelength=1000, n=0, filter_low_values=False):
        """generates a list of all wavelengths with the sum of their prominences every time they are one of the top
        
        params:
            global_spectrum: if not loading from database, the dataset to use.
                                Should be a dataframe with columns "pc_time_end_measurement" and "global_spectrum"
            column_name: if loading from database, the column containing the spectral data
            cutoff_angle: if loading from database, the zenith angle to include(radians)
            cutoff_wavelength: the meax wavlength to include, usefull for cropping out extreme noise
            n: how many dips to take from each measurement, if 0, uses all
                                if too low when working with a single spectrum, not enough dips and some segments will be empty(errors)
            filter_low_values: wether or not to filter out spectra with low total intensities, 
                                used to filter out night time data, but will also filter out shaded data
        returns:
            weighted_frequency: a graph showing where dips appear over the dataset, weighted by their prominence
        """
        ##### load from databse if no spectrum is provided
        if global_spectrum is None or len(global_spectrum) == 0:
            ##### some databses may not have precalculated data loaded
            try:
                global_spectrum = self.driver.db_load.load(["pc_time_end_measurement", column_name], condition="sza < "+str(cutoff_angle))
            except:
                global_spectrum = self.driver.db_load.load(["pc_time_end_measurement", column_name])
                
            global_spectrum = global_spectrum.rename(columns={column_name:"global_spectrum"})
            global_spectrum = self.driver.reformat.deserialise(global_spectrum, "global_spectrum")
        
        if filter_low_values:
            selection = []
            for j in range(len(global_spectrum)):
                if np.sum(global_spectrum.loc[j, "global_spectrum"]) > 10000:
                    selection.append(True)
                else:
                    selection.append(False)
            global_spectrum = global_spectrum.loc[selection, :].reset_index()
        
        global_spectrum = global_spectrum["global_spectrum"].values
        
        nlargest, nlargest_prominence = [], []
        
        if n==0:
            ##### if no restrictions, find all peaks
            nn = (None, None)
            for spectrum in global_spectrum:
                if not self.find_peaks:
                    spectrum = -spectrum
                largest, properties = sp.signal.find_peaks(spectrum, prominence=nn)
                nlargest += list(largest)
                nlargest_prominence += list(properties["prominences"])
            nlargest = np.array(nlargest)
            nlargest_prominence = np.array(nlargest_prominence)
            
        else:
            nlargest, nlargest_prominence = SpectrumUtils.find_nlargest(global_spectrum, n, ["wavelengths", "prominences"], cutoff_wavelength, offset=0, find_peaks=self.find_peaks)
        
        weighted_frequency = np.zeros(801)
        ##### add the found dips to the weighted spectrum
        for i in range(len(nlargest)):
            weighted_frequency[nlargest[i]] += nlargest_prominence[i]
        
        
        return weighted_frequency
    
    
    def calculate_segment_calibration(self, centre_point, dist_from_centre, 
                                      c0_lim=20, c1_lim=0.05, iterations=30, 
                                      init_c0_lim=50, init_c0=0, 
                                      plot_attempts=False):
        """loops through the spectrum and finds the linear calibration for each segment
        params:
            centre_point: The point in the reference spectrum where the calibration starts from. Ideally should be a large, identifiable dip.
            dist_from_centre: When splitting the spectrum into segments, how far the segments should extend from the centre of the segment
                            controls the segment width
            c0_lim: When finding a segment's linear calibration, the range of values to check while shifting left/right
            c1_lim: When finding a segment's linear calibration, the range of stretches to test.
            iterations: How many different stretch values to try within the limit (every integer shift is tried within the limits)
            initial_c0_limit: how far to look from the reference centre_point to look for the corresponding peak
            plot_attempts: plot the individual calibrated segment and all the attempted calibration values with their fit quality
        """
        c0 = 0
        c1 = 1
        
        if init_c0 is not None:
            c0 = init_c0
        
        result = {}
        attempts = {}
        attempts_params = {}
        
        if centre_point < 0 or centre_point > 800:
            raise ValueError("centre_point must be within spectrum")
        
        ##### create centre segment and calculate calibration
        segment = WeightedSpectrumSegment(self.weighted_reference, self.spectrum, 
                                          centre_point, dist_from_centre, centre_point)
        first_cal, new_attempts = segment.find_best_calibration(c0, c1, init_c0_lim, c1_lim, iterations=iterations, plot=False, debug=True)
        
        ##### adds the result and metadata to a list
        result[centre_point] = first_cal
        attempts[centre_point] = new_attempts
        attempts_params[centre_point] = [0, 1]
        
        
        ##### right side
        ##### initial values are from centre segment
        right_centre_point = centre_point
        new_cal = [first_cal[0], first_cal[1]]
        while right_centre_point < len(self.spectrum)-2*dist_from_centre:
            old_centre_point = right_centre_point
            right_centre_point += 2*dist_from_centre
            
            attempts_params[right_centre_point] = new_cal
            
            ##### create a new segment to the right of the previous segment
            ##### use the gradient from previous segment as a starting point
            segment = WeightedSpectrumSegment(self.weighted_reference, self.spectrum, right_centre_point, dist_from_centre, old_centre_point)
            

            new_cal, new_attempts = segment.find_best_calibration(new_cal[0], new_cal[1], c0_lim, c1_lim, iterations=iterations, debug=True)
            
            
            result[right_centre_point] = new_cal
            attempts[right_centre_point] = new_attempts
        
        
        
        ##### left side
        ##### initial values are from centre segment
        left_centre_point = centre_point
        new_cal = [first_cal[0], first_cal[1]]
        while left_centre_point > 2*dist_from_centre:
            old_centre_point = left_centre_point
            left_centre_point -= 2*dist_from_centre
            
            attempts_params[left_centre_point] = new_cal
            
            ##### create a new segment to the left of the previous segment
            ##### use the gradient from previous segment as a starting point
            segment = WeightedSpectrumSegment(self.weighted_reference, self.spectrum, left_centre_point, dist_from_centre, old_centre_point)
            
            new_cal, new_attempts = segment.find_best_calibration(new_cal[0], new_cal[1], c0_lim, c1_lim, iterations=iterations, debug=True)
            
            result[left_centre_point] = new_cal
            attempts[left_centre_point] = new_attempts

        self.calibration = result
        
        
        
        if plot_attempts:
            self.plot_attempts(attempts, attempts_params, c0_lim, c1_lim, iterations, dist_from_centre, init_c0_lim)
        

    
    def combine_segments(self, dist_from_centre):
        """combines the calibrated segments into one spectrum
        params:
            dist_from_centre: distance from the centre to the edge of the segment
        """
        ##### creates a spectrum of zeros that will be overwritten
        final_spectrum = np.zeros(len(self.spectrum))
        
        ##### loops through each centre point
        keys = list(self.calibration.keys())
        keys.sort()
        for key in keys:
            ##### calibrates the individual segment
            new_cal = self.calibration[key]
            calibrated = self.ps.apply_origin_wavelength_calibration(self.spectrum, (0, new_cal[1], 0, 0), key)
            calibrated = self.ps.apply_constant_wavelength_calibration(calibrated, new_cal[0])
            
            #### adds the calibrated segment to the final sepctrum
            left_edge = max(0, key-dist_from_centre)
            right_edge = min(len(calibrated), key+dist_from_centre)
            final_spectrum[left_edge:right_edge] = calibrated[left_edge:right_edge]
        
        self.calibrated_spectrum = final_spectrum
    
    
    
    def find_n_peaks(self, spectrum, n=None):
        """find the n largest peaks in a spectrum
        params:
            spectrum: spectrum containing peaks
            n: number of peaks to find. if none returns all
        returns:
            reference_peaks: the index of all the peaks
        """
        spectrum = spectrum/max(np.abs(spectrum))
        peaks, properties = sp.signal.find_peaks(spectrum, prominence=(None, None))
        prominences = properties["prominences"]
        
        ##### sorts by most prominent peak
        index = np.flip(prominences.argsort())
        
        if n == None:
            n = len(peaks)-1
        n = min(len(peaks)-1, n)

        reference_peaks = peaks[index][:n]
        return reference_peaks
    
    def decalibrate_linear_segment(self, ref_peak, cal_peak):
        """undoes the linear calibration at a point"""
        cal = self.calibration
        centres = np.array(list(cal.keys()))
        
        ##### finds which calibration has been applied
        closest_centre_index = np.argmin(np.absolute(centres-ref_peak))
        closest_centre = centres[closest_centre_index]
        segment_cal = cal[closest_centre]
        
        ##### calibration was done around the centre point, so find position relative to centre_point
        #####   then decalibrate around 0, then add back the centre point
        centre_dist = cal_peak-closest_centre
        decalibrated = -SpectrumUtils.apply_inverse_polynomial(centre_dist, segment_cal[0], segment_cal[1], segment_cal[2], segment_cal[3])
        
        decalibrated_peak = closest_centre - decalibrated
        
        return decalibrated_peak
    
    
    def match_fit_quality(self, params, ref, measured):        
        c0 = params["c0"].value
        c1 = params["c1"].value
        c2 = params["c2"].value
        c3 = params["c3"].value
        return ref-SpectrumUtils.apply_inverse_polynomial(measured, c0, c1, c2, c3)
    
    def match_dips(self, reference_data, measured_data, method="least_squares"):
        params = lmfit.Parameters()
        params.add('c0', value=1620)#, min=-20, max=20)
        params.add('c1', value=-1.4)#, min=-1.6, max=-1.2)
        params.add('c2', value=0.0)#, min=-0.0000001, max=0.00000001)
        params.add('c3', value=0.0)
        ##### limit c3  to be negative
        ##### when applying inverse polynomials, 
        #####   there is no way to be sure which value to pick when interpolating from a non 1-1 function(one that has seperate maxima and minima)
        ##### so the polynomials are limited to decreasing functions, which will always be 1-1 in this case
        
        result = lmfit.minimize(self.match_fit_quality, params, kws = {"ref":reference_data, "measured":measured_data}, method=method)
        
        ##### unpack results
        c0_result = result.params["c0"].value
        c1_result = result.params["c1"].value
        c2_result = result.params["c2"].value
        c3_result = result.params["c3"].value
        
        return [c0_result, c1_result, c2_result, c3_result]
    
    def match_n_dips(self, n, left_limit=0, nlargest=None, reference_dip_locations=None):
        """matches dips between the reference and the linear calibrated spectrum, then converts to pixel position
        params:
            n: number of dips to match
            left_limit: the leftmost dip to consider, as SMARTS spectrum extends further left than is measured
            nlargest: how many peaks to choose from from the calibrated spectrum, can help avoid matching with tiny dips
        returns:
            reference_peaks: the matched_dips' location in the reference spectrum
            measured_peaks: the corresponding position in the uncalibrated pixel spectrum
        """
        ##### finds all the largest peaks from the reference data
        calibrated_peaks = self.find_n_peaks(self.calibrated_spectrum, nlargest)
        
        reference_peaks = np.array(reference_dip_locations)
        if reference_dip_locations is None:
            ##### takes the n largest peaks from the reference data that are past the left_limit
            reference_peaks = self.reference_peaks[self.reference_peaks >= left_limit][:n]
        else:
            n = len(reference_dip_locations)
            reference_peaks -= 300
        
        calibrated_peaks = np.sort(calibrated_peaks)
        reference_peaks = np.sort(reference_peaks)
        
        ##### finds the closest measured peaks to the reference peaks
        matched_peaks_index = [np.argmin(np.absolute(calibrated_peaks-peak)) for peak in reference_peaks]
        matched_peaks = calibrated_peaks[matched_peaks_index]
        
        # print(matched_peaks)
        
        ##### convert the found peaks back into pixel data
        measured_peaks= []
        for i in range(len(reference_peaks)):
            ref_peak = reference_peaks[i]
            cal_peak = matched_peaks[i]
            
            ##### undoes the linear calibration
            decalibrated_peak = self.decalibrate_linear_segment(ref_peak, cal_peak)
            # print(decalibrated_peak)
            
            ref_peak += 300
            decalibrated_peak += 300
            
            ##### undoes the previous calibration
            if self.applied_poly is not None:
                decalibrated_peak = SpectrumUtils.apply_polynomial(decalibrated_peak, self.applied_poly[0], self.applied_poly[1], self.applied_poly[2], self.applied_poly[3])
            
            measured_peaks.append(decalibrated_peak)
        measured_peaks = np.array(measured_peaks)
        
        # print(measured_peaks)
        
        return reference_peaks, measured_peaks
    
    
    
    def plot_attempts(self, attempts, attempts_params, c0_lim, c1_lim, iterations, dist_from_centre, init_c0_lim):
        """For each segment, plots the found linear calibration and a histogram of all tested value pairs
        params:
            attempts: a dictionary with keys corresponding to the centre of each segment,
                        containing a 2d array of the fit quality for each tested value
            attempt_params: a dictionary with keys corresponding to the centre of each segment,
                        containing the starting point for each segment's calibration [c0, c1]
            c0_lim: When finding a segment's linear calibration, the range of values to check while shifting left/right
            c1_lim: When finding a segment's linear calibration, the range of stretches to test.
            dist_from_centre: When splitting the spectrum into segments, how far the segments should extend from the centre of the segment
                        controls the segment width
            iterations: How many different stretch values to try within the limit (every integer shift is tried within the limits)
            init_c0_lim: initial c0 limit when finding main peak
        """
        unsorted_keys = list(self.calibration.keys())
        centre = unsorted_keys[0]
        keys = unsorted_keys.copy()
        keys.sort()
        for key in keys:
            new_cal = self.calibration[key]
            calibrated = self.ps.apply_origin_wavelength_calibration(self.spectrum, (0, new_cal[1], 0, 0), key)
            calibrated = self.ps.apply_constant_wavelength_calibration(calibrated, new_cal[0])
            
            ##### calculate the windowed reference to plot with the calibrated spectrum
            reference = self.weighted_reference/max(self.weighted_reference)
            segment = reference[max(0, key-dist_from_centre):key+dist_from_centre]
            
            left_padding_dist = max(0, key-dist_from_centre)
            right_padding_dist = max(0, len(self.weighted_reference)-(key+dist_from_centre))
            
            windowed_reference = np.concatenate((np.zeros(left_padding_dist), segment, np.zeros(right_padding_dist)))
            if max(windowed_reference) > 0:
                windowed_reference = windowed_reference/max(windowed_reference)
            
            ##### plot the spectrum after the found calibration and the weighted reference
            plt.figure(figsize=(20, 10))
            plt.plot(windowed_reference, label="reference")
            plt.plot(calibrated/max(calibrated), label="calibrated")
            plt.axvline(key, c="black")
            plt.axvline(key+dist_from_centre, c="gray")
            plt.axvline(key-dist_from_centre, c="gray")
            plt.suptitle("Shift: "+str(new_cal[0]) + "\n Stretch: " + str(np.round(new_cal[1], 2)))
            plt.legend()
            plt.show(block=False)
            
            ##### prepare data to plot all attempted shift and stretch values with fit quality
            this_attempts = attempts[key]
            this_attempts = np.flip(this_attempts, axis=0)
            init_values = attempts_params[key]
            
            plt.figure(figsize=(20,10))
            plt.imshow(this_attempts)
            
            ##### if centre and c0 known, plot hist as line not rectangle
            single = False
            if len(this_attempts[0]) == 1:
                single = True
            
            this_c0_lim = c0_lim
            if key == centre:
                this_c0_lim = init_c0_lim
            
            ##### calculates the xticks and labels and plots them
            if not single:
                shift_range = np.arange(init_values[0]-this_c0_lim, init_values[0]+this_c0_lim+1)
                x = np.linspace(0, len(shift_range)-1, 9).astype(int)
                plt.xticks(x, shift_range[x])
                plt.xlabel("shift")
            if single:
                plt.xticks([])
            
            ##### plots the yticks and labels
            stretch_range = np.linspace(init_values[1]-c1_lim, init_values[1]+c1_lim, iterations).round(3)
            stretch_range = np.flip(stretch_range)
            y = np.linspace(0, len(stretch_range)-1, 9).astype(int)
            plt.yticks(y, stretch_range[y])
            plt.ylabel("stretch")
            plt.suptitle(self.name+"\n segment centre point: "+str(key))
            
            plt.show(block=False)
    
    def plot_segmented_calibration(self, dist):
        """plots all the linear calibrations in the segment they are used"""
        segmented_cal = self.calibration
        keys = list(segmented_cal.keys())
        
        plt.figure(figsize=(20,10))
        for key in keys:
            poly = segmented_cal[key]
            x_data = np.arange(key-dist, key+dist)
            y_data = []
            for i in range(len(x_data)):
                y_data.append(SpectrumUtils.apply_polynomial(x_data[i], poly[0], poly[1], poly[2], poly[3]))
            y_data = np.array(y_data).round().astype(int)
            plt.scatter(x_data, y_data, s=1, c="tab:blue")
        plt.suptitle(self.name+" "+ "segmented wavelength calibration")
        plt.show(block=False)
    
    def plot_segmented_linear_calibration(self, dist_from_centre):
        """plot the combination of all segments with their linear calibration, 
        a first guess at the calibration so dips can be matched"""
        weighted_reference = np.concatenate((np.zeros(300), self.weighted_reference))
        calibrated_spectrum = np.concatenate((np.zeros(300), self.calibrated_spectrum))
        
        plt.figure(figsize=(20, 10))
        plt.plot(weighted_reference/max(weighted_reference), label="reference")
        # plt.plot(self.spectrum/max(self.spectrum), label="measured")
        plt.plot(calibrated_spectrum/max(calibrated_spectrum), label="segmented linear calibration")
        
        for wavelength in self.calibration:
            wavelength += 300
            plt.axvline(wavelength, color="lightgray")
            plt.axvline(wavelength+dist_from_centre, color="black")
            plt.axvline(wavelength-dist_from_centre, color="black")
            plt.annotate((str(round(self.calibration[wavelength-300][0]))+", "+str(round(self.calibration[wavelength-300][1], 4))+"x"), [wavelength, 1])
        
        plt.xlim(self.graph_limits[0], self.graph_limits[1])
        plt.yticks([])
        plt.ylabel("wavelength")
        plt.suptitle(self.name+" "+ "initial segmented linear calibration")
        plt.legend()
        plt.show(block=False)
    
    def plot_matched_dips(self, ref, measured):
        """plots the dips that have been found onto their corrseponding spectra, 
        usedul for checking that the right dips have been matched to each other"""
        ref_spectrum = np.concatenate((np.zeros(300), self.weighted_reference/max(self.weighted_reference)))
        
        ##### use wavelength spectrums if they are available
        if self.reference is not None:
            ref_spectrum = np.concatenate((np.zeros(300), self.reference/max(self.reference)))
        
        ref_string = "\nReference dips:   "
        measured_string = "\nMeasured dips: "
        for _ref, _measured in zip(ref.astype(str), measured.astype(str)):
            ref_string += str(_ref) + ","
            ref_string += " "*(4-len(_ref)) if len(_ref) < 4 else ""
            measured_string += str(_measured) + ","
            measured_string += " "*(4-len(_measured)) if len(_measured) < 4 else ""
        
        
        measured = np.flip(measured)
        
        plt.figure(figsize=(20, 10))
        plt.plot(ref_spectrum, label="reference")
        plt.plot(self.pixel_spectrum, label="measured")
        plt.scatter(ref, ref_spectrum[ref.astype(int)])
        plt.scatter(measured, self.pixel_spectrum[measured])
        plt.ylim(0, 1)
        plt.yticks([])
        plt.ylabel("wavelength")
        plt.suptitle(self.name+" "+ "selected dips" + ref_string[:-2] + measured_string[:-2])
        plt.legend()
        plt.show(block=False)
    
    def plot_calibration(self, measured, poly):
        """plots the calibration polynomial, with the dips used to find it"""
        calibrated_dips = np.array([SpectrumUtils.apply_inverse_polynomial(x, poly[0], poly[1], poly[2], poly[3]) for x in measured]).round().astype(int)
        cal_string = f"{poly[3]:.2e}x^3 + {poly[2]:.2e}x^2 + {poly[1]:.2f}x + {poly[0]:.2f}"
        
        plt.figure(figsize=(20, 10))
        plt.scatter(measured, calibrated_dips)
        if self.applied_poly is not None:
            plt.plot(self.ps.apply_wavelength_calibration(np.arange(0, 1200), self.applied_poly, inverse=True), np.arange(300, 1101), label="old calibration")
        plt.plot(self.ps.apply_wavelength_calibration(np.arange(0, 1200), poly, inverse=True), np.arange(300, 1101), label="calibration")
        plt.xlim(0, 1200)
        plt.suptitle(self.name+" "+ "calibration: \n" + cal_string)
        plt.xlabel("pixels")
        plt.ylabel("wavelength")
        plt.legend()

        plt.show(block=False)

    
    def get_calibrated_spectrum(self, poly):
        calibrated_spectrum = self.ps.apply_wavelength_calibration(self.pixel_spectrum, poly, inverse=True, flip=True)
        if self.amplitude_calibration is not None:
            calibrated_spectrum = self.ps.apply_amplitude_calibration(calibrated_spectrum, self.amplitude_calibration)
            calibrated_spectrum = calibrated_spectrum/max(calibrated_spectrum)
        calibrated_spectrum = np.concatenate((np.zeros(300), calibrated_spectrum))
        return calibrated_spectrum
    
    def plot_calibrated_spectrum(self, poly, comp_ref, comp_measured, reference_dip_locations):
        """calibrates the pixel spectrum with the old and the new calibration and plots them against the reference"""
        
        plt.figure(figsize=(20,10))
        
        ##### adds 300 zeros to the start of the spectrum and sets the xlim at 300, so the graph starts at 300, not 0
        reference = np.concatenate((np.zeros(300), self.reference))
        plt.plot(reference/max(reference), label="reference")
        
        original_label = "original calibration"
        if self.source == "pixel_spectra":
            original_label = "default calibration"
        original_calibrated_spectrum = self.get_calibrated_spectrum(self.applied_poly)
        plt.plot(original_calibrated_spectrum, label=original_label)
        
        calibrated_spectrum = self.get_calibrated_spectrum(poly)
        plt.plot(calibrated_spectrum/max(calibrated_spectrum), label="calibrated")
        
        for dip in comp_ref:
            plt.axvline(dip, c="lightgray")
        
        
        
        
        plt.xlim(self.graph_limits[0], self.graph_limits[1])
        plt.ylim(0, 1)
        plt.yticks([])
        plt.ylabel("amplitude")
        plt.xlabel("wavelength")
        plt.suptitle(self.name+" "+ "First measurement calibrated")
        plt.legend()
        plt.show(block=False)
        
        # calibrated_dataset = self.ps.apply_wavelength_calibration(self.wavelength_spectra, poly, np.arange(300, 1101), output_shape=[300, 1101])
        
        # graph = Graph()
        # graph.daily_peaks_density(calibrated_dataset, reference_lines=np.sort(ref), reference_labels=[])
        
        # try:
        #     graph.daily_peaks_density(calibrated_dataset, reference_lines=np.sort(ref), reference_labels=[])
        # except ValueError as e:
        #     if e == "histogram needs multiple days of data":
        #         print("pass more data to get summary plot")
        #     else:
        #         print("unknown exception")
    
    
    def compare_dips(self, poly, reference_dip_locations, left_limit, n):
        calibrated_spectrum = self.get_calibrated_spectrum(poly)
        
        reference_peaks = np.array(reference_dip_locations)
        if reference_dip_locations is None:
            ##### takes the n largest peaks from the reference data that are past the left_limit
            reference_peaks = self.reference_peaks[self.reference_peaks >= left_limit][:n]
        else:
            reference_peaks -= 300
        reference_peaks += 300
        calibrated_peaks = self.find_n_peaks(-calibrated_spectrum+max(calibrated_spectrum))
        
        
        calibrated_peaks = np.sort(calibrated_peaks)
        reference_peaks = np.sort(reference_peaks)
        
        if len(calibrated_peaks) == 0:
            return np.array([]), np.array([])
        
        
        
        ##### finds the closest measured peaks to the reference peaks
        matched_peaks_index = [np.argmin(np.absolute(calibrated_peaks-peak)) for peak in reference_peaks]
        matched_peaks = calibrated_peaks[matched_peaks_index]
        
        return reference_peaks, matched_peaks
        
        
        
    
    def plot_error(self, poly, ref, measured, unrounded):
        unrounded = [SpectrumUtils.apply_inverse_polynomial(x, poly[0], poly[1], poly[2], poly[3]) for x in unrounded]
        
        if len(ref) != len(unrounded) or len(measured) != len(unrounded):
            return
        
        error = measured-ref
        
        plt.figure(figsize=(20, 10))
        plt.plot(ref, error)
        plt.scatter(ref, error)
        for x, y in zip(ref, error):
            plt.annotate(f"{x:.0f}", (x, y))
        plt.plot(ref, np.sort(unrounded)-ref)
        plt.show(block=False)
    
    
    
    def find_calibration(self, centre_point=760, dist_from_centre=50, 
                         num_dips=15, 
                         c0_lim=10, c1_lim=0.1, iterations=50, 
                         init_c0_lim=30, init_c0=0, 
                         left_cutoff=360, 
                         reference_dip_locations=None, 
                         plot_debug=False, plot_results=True, plot_summary=False,
                         return_dips=False, 
                         **kwargs):
        """finds the best calibration from pixels to wavelengths.
        
        params:
            centre_point: The point in the reference spectrum where the calibration starts from. Ideally should be a large, identifiable dip.
            init_c0_limit: if lin_cal is not set, how far to look from the reference centre_point to look for the corresponding peak
            dist_from_centre: When splitting the spectrum into segments, how far the segments should extend from the centre of the segment
                            controls the segment width
            left_cutoff: When selecting dips to match, the minimum reference wavelength to pick, 
                            as the measured spectrum drops off at 350nm,whereas SMARTS has data down to 300nm, 
                            so dips could being selected that arent in the measured data.
                            Should be the reference equivalent of the measured limit
            num_dips: number of dips to match between reference data and measured data
            c0_lim: When finding a segment's linear calibration, the range of values to check while shifting left/right
            c1_lim: When finding a segment's linear calibration, the range of stretches to test.
            iterations: How many different stretch values to try within the limit (every integer shift is tried within the limits)
            plot_debug: For each segment, plots the found linear calibration and a histogram of all tested value pairs
            plot_results: plots a selection of graphs giving an ovewrview of each step of the process and the accuracy of the calibration
        
        returns:
            poly: list containing the values that are the coefficint for the found polynomial
                            [c0, c1, c2, c3]
        """
        if not self.num_reference_dips >= num_dips:
            raise ValueError("num_reference_dips must be >= num_dips")
            
        
        ##### convert from wavelength to index
        centre_point -= 300
        left_cutoff -= 300
        
        ##### calculate the linear calibration for each segment of the spectrum
        self.calculate_segment_calibration(centre_point, dist_from_centre, c0_lim=c0_lim, c1_lim=c1_lim, iterations=iterations, init_c0_lim=init_c0_lim, init_c0=init_c0, plot_attempts=plot_debug)
        ##### combines the linear calibrated segments into one spectrum that is close to being calibrated
        self.combine_segments(dist_from_centre)
        if sum(self.calibrated_spectrum>0) < num_dips:
            if return_dips:
                return None, None
            return None
        ##### find n pairs of dips that correspond between the reference data and the pixel data
        if reference_dip_locations is not None:
            num_dips = len(reference_dip_locations)
        
        ref, measured = self.match_n_dips(num_dips, left_cutoff, reference_dip_locations=reference_dip_locations)
        if len(measured) != num_dips:
            if return_dips:
                return None, None
            return None
        
        unrounded = measured
        measured = measured.round().astype(int)
        
        
        
        ##### converting from index space to wavelength space
        ref += 300
        
        poly = self.match_dips(ref, measured)
        
        self.poly_cal = poly
        
        comp_ref, comp_measured = self.compare_dips(poly, reference_dip_locations, left_cutoff, num_dips)
        
        
        if plot_results:
            self.plot_segmented_linear_calibration(dist_from_centre)
            self.plot_matched_dips(ref, measured)
            self.plot_calibration(measured, poly)
            self.plot_calibrated_spectrum(poly, comp_ref, comp_measured, reference_dip_locations)
            self.plot_error(poly, comp_ref, comp_measured, unrounded)
        elif plot_summary:
            self.plot_calibrated_spectrum(poly, comp_ref, comp_measured, reference_dip_locations)
            
        if return_dips:
            return poly, (comp_ref, comp_measured)
        return poly
        
        
        