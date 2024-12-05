# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

def apply_polynomial(x, c0, c1, c2, c3):
    # return c3*x**3 + c2*x**2 + c1*x + c0
    return np.polyval([c3, c2, c1, c0], x)


def apply_inverse_polynomial(y, c0, c1, c2, c3,
                             target_point=600,
                             density=10,
                             sample_x_min=-1000, sample_y_max=2000):
    """for a given value y and a polynolmial, finds the value x that when transformed by the polynomial, gives y
    generates a sample of x and y data, and interpolates.
        but interpolation only works in a 1 to 1 graph (if each y point corresponds to multiple x points, which do you choose?)
        Most of this function is spent finding the segment of the graph that is one-one, and can be interpolated along
        by default it is the segment containg x=600, as that is in the middle of the spectrum, so will likley give the correct polynomial segment
    """
    sample_x = np.arange(sample_x_min, sample_y_max, 1/density)
    sample_y = np.polyval([c3, c2, c1, c0], sample_x)
    
    ##### finite differentiation(array of differences)
    grad = np.gradient(sample_y)
    
    ##### checks if polynomial is already 1-1
    ##### if gradient never crosses 0 -> is never flat -> never changes direction -> 1-1
    if (grad > 0).all() or (grad < 0).all():
        segment_x = sample_x
        segment_y = sample_y
    else:
        midpoint_index = None
        increasing_segment_x = None
        increasing_segment_grad = None
        ##### gradient formula = 3c3x^2 + ...
        #####  so if gradient c2 has the same sign as poly c3
        ##### if gradient c2 is pos, gradient is u-shaped, if negative, n-shaped
        if c3 >= 0:
            ##### gradient has minima
            midpoint_index = np.argmin(grad)
            
            ##### finds half of the gradient that is 1-1(either side of the minima/maxima is 1-1)
            increasing_segment_x = sample_x[midpoint_index:]
            increasing_segment_grad = grad[midpoint_index:]
        elif c3 < 0:
            ##### gradient has maxima
            midpoint_index = np.argmax(grad)
            
            ##### finds half of the gradient that is 1-1(either side of the minima/maxima is 1-1)
            increasing_segment_x = sample_x[:midpoint_index]
            increasing_segment_grad = grad[:midpoint_index]
        
        ##### finds the value where gradient is 0, poly is flat
        zero_pos = np.interp(0, increasing_segment_grad, increasing_segment_x)
        
        ##### x^2 is symetrical, find the other x-intercept, using the midpoint
        dist_from_mid = (zero_pos-sample_x[midpoint_index])
        zero_pos_2 = sample_x[midpoint_index] - dist_from_mid
        
        ##### convert values to index position
        zero_pos_index = int(midpoint_index + dist_from_mid*density)
        ##### index cant be less than 0 or more than length of array
        #####  this happens when only 1 turning point is within range
        zero_pos_2_index = min(len(sample_x), max(0, int(midpoint_index - dist_from_mid*density)))
        
        zero_pos = int(zero_pos)
        zero_pos_2 = int(zero_pos_2)
        
        
        ##### find the segment of the polynomial that is 1-1 and contains the target_pointx
        ##### if target point is to right of both turning points, use segment = rightmost turning point onwards
        if zero_pos <= target_point and zero_pos_2 <= target_point:
            segment_x = sample_x[max(zero_pos_index, zero_pos_2_index):]
            segment_y = sample_y[max(zero_pos_index, zero_pos_2_index):]
        ##### if target point is to left of both turning points, use segment = sample_x until leftmost turning point
        elif zero_pos >= target_point and zero_pos_2 >= target_point:
            segment_x = sample_x[min(zero_pos_index, zero_pos_2_index):]
            segment_y = sample_y[min(zero_pos_index, zero_pos_2_index):]
        ##### target point must be inbetween
        elif zero_pos <= zero_pos_2:
            segment_x = sample_x[zero_pos_index:zero_pos_2_index]
            segment_y = sample_y[zero_pos_index:zero_pos_2_index]
        elif zero_pos >= zero_pos_2:
            segment_x = sample_x[zero_pos_2_index:zero_pos_index]
            segment_y = sample_y[zero_pos_2_index:zero_pos_index]
    
    
    result = None
    if segment_y[0] > segment_y[-1]:
        ##### decreasing
        result = np.interp(y, np.flip(segment_y), np.flip(segment_x), left = 12345, right=-12345)
    else:
        ##### increasing
        result = np.interp(y, segment_y, segment_x, left = 12345, right=-12345)
    
    return result

def read_simple_file(filepath):
    """rands a simple file, one float per line"""
    data = []
    with open(filepath, "r") as f:
        data = f.readlines()

    for i in range(len(data)-1):
        data[i] = float(data[i][:-1])
    
    data[len(data)-1] = float(data[len(data)-1])

    data = np.array(data)
    
    return data

def read_reference_file(filepath):
    """reads a csv file containing a reference spectrum"""
    data = pd.read_csv(filepath, sep="\t")
    ordered = np.interp(np.arange(300, 1100), data["wavelength"], data["average"])
    return ordered

def read_smarts_file(filepath):
    raise NotImplementedError("change to read_simple_file()")

def read_amplitude_file(file_path):
    ##### read calibration data as df
    data = pd.read_csv(file_path, sep="\t", header=None)
    data.columns = ["wavelength_pos", "calibration"]
    
    ##### average out duplicate wavelength calibrations
    data = data.groupby("wavelength_pos").mean()
    data = data.reset_index()
    
    ##### convert to 1d numpy array
    calibration_array = data["calibration"].to_numpy()
    return calibration_array


def add_curves_to_graph(graph, curve, scale):
    plt.plot(graph)
    plt.show(block=False)
    plt.plot(curve)
    plt.show(block=False)
    
    
    curve_mid = int(len(curve)/2)
    
    max_value = max(graph)
    graph /= max_value
    
    for i in range(len(graph)):
        new_graph = np.zeros(len(graph))
        start = max(0, i-curve_mid)
        stop = min(len(graph), i+curve_mid)
        
        curve_start = max(0, curve_mid-i)
        curve_stop = min(len(curve), len(graph)-i)
        
        new_graph[start:stop] += curve[curve_start:curve_stop]
        plt.plot(new_graph)
        plt.show(block=False)

def poly_to_string(poly):
    return f"{poly[3]:.2e}x^3 + {poly[2]:.2e}x^2 + {poly[1]:.2f}x + {poly[0]:.2f}"


def find_nlargest(spectra, n, properties_to_find:[str], cutoff_wavelength, offset=300, find_peaks=False, fill_nan=False):
    """given a spectrum, find the n largest dips for each measurement
    params:
        spectra: dataframe containing one spectrum per row
        n: how many dips to pick per measurement
        properties_to_find: list of all properties to find, should always include prominences and wavelengths
        cutoff_wavelength: the maximum wavelength included
    """
    
    if type(cutoff_wavelength) in [int, float]:
        cutoff_wavelength = (offset, cutoff_wavelength)
        
    ##### generate base output array
    output_array = []
    for i in range(len(properties_to_find)):
        output_array.append([])
        
    ##### for each spectrum
    for spectrum in spectra:
        
        ##### cutoff wavelength
        spectrum = spectrum[(cutoff_wavelength[0]-offset):(cutoff_wavelength[1]-offset)]
        
        if not find_peaks:
            spectrum = -spectrum
        
        ##### find dips
        nn = (None, None)
        dips, properties = signal.find_peaks(spectrum, prominence=nn, width=nn)
        
        if n==0:
            new_n = len(dips)
        else:
            new_n = n
        
        if type(spectrum) == type(np.nan):
            for j in range(len(output_array)):
                output_array[j] += [np.nan]*new_n
            continue
        
        
        ##### convert from index to wavelength
        properties["wavelengths"] = dips+offset
        ##### add all the properties to a list
        data_list = []
        
        
        for _property in properties_to_find:
            data_list.append(properties[_property])
        
        ##### find the correct order of data, sorted by prominence
        #####   argsort so the same sort can be used on the other rows
        indexes = properties["prominences"].argsort()
        
        
        for j in range(len(properties_to_find)):
            ##### apply the sort and take the n most prominent
            data_list[j] = np.take_along_axis(np.array(data_list[j]), indexes, 0)[-new_n:]
            num_dips = len(data_list[j])
            if num_dips != n:
                data_list[j] = list(data_list[j])+[np.nan]*(n-num_dips)
            output_array[j] += list(data_list[j])
        
    
    for i, array in enumerate(output_array):
        output_array[i] = np.array(array)
    return output_array


def read_wavelength_polys(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        lines[i] = lines[i].split(sep="\t")
    
    wavelength_polys = {}
    for line in lines:
        if line[0] == "WavelengthPoly":
            values = line[2:6]
            for i in range(len(values)):
                values[i] = float(values[i])
            wavelength_polys["channel_"+str(line[1])] = values
    
    return wavelength_polys

def format_output(cals, filepath):
    if os.path.dirname(filepath) != '':
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        with open(filepath, "w") as f:
            cals["average"] = np.array([0.0, 0.0, 0.0, 0.0])
            for channel in list(cals.keys())[:-1]:
                data = cals[channel]
                f.write("WavelengthPoly\t"+str(channel)[-1] +"\t"+ str(data[0]).replace("e", "E")+"\t"+str(data[1]).replace("e", "E")+"\t"+str(data[2]).replace("e", "E")+"\t"+str(data[3]).replace("e", "E")+"\n")
                
                ##### add current row to average
                if channel[-2] == "_" and int(channel[-1]) in np.arange(1, 8):
                    cals["average"] += np.array(data)
            
            cals["average"] = cals["average"]/7
            data = cals["average"]
            f.write("\nWavelengthPoly\tav(1-7)\t"+ str(data[0]).replace("e", "E")+"\t"+str(data[1]).replace("e", "E")+"\t"+str(data[2]).replace("e", "E")+"\t"+str(data[3]).replace("e", "E")+"\n")
                    
    except PermissionError as e:
        raise PermissionError("Permission to store results was denied, this is usually caused by trying to store directly to the root folder \n"+
                              str(e))


def apply_inverse_polynomial_a(y, c0, c1, c2, c3, flip=True):
    sample_x = np.arange(-2400, 2401)
    sample_y = apply_polynomial(sample_x, c0, c1, c2, c3)
    plt.plot(sample_x, sample_y)
    plt.axhline(y)
    
    sample_x = np.flip(sample_x)
    if flip:
        sample_y = np.flip(sample_y)
    
    corresponding_pixels = np.interp(y, sample_y, sample_x, right=12345, left = -12345)
    plt.axvline(corresponding_pixels)
    plt.show(block=False)
    return corresponding_pixels
