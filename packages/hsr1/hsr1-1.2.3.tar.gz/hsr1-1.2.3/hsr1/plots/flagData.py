# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import pandas as pd
import numpy as np

all_columns = ["global_integral", "diffuse_integral", "direct_normal_integral",
               "sza", "toa_hi"]
    
def flag(df:pd.DataFrame, ignore_nights:bool=True):
    """generates a dataframe of each reading and wether that reading is flagged in each specific check
    params:
        df: dataframe columns: ["global_integral", "diffuse_integral", "direct_normal_integral", "sza", "toa_hi"]
        ignore_nights: if true, dosen't flag night data(sza<90)
    """
    limits = pd.DataFrame(index=df.index)
    flags = pd.DataFrame(index=df.index)
    
    columns = df.columns
    if "sza" in columns:
        limits["mu0"] = np.cos(df["sza"])
        if "toa_hi" in columns:
            limits["toa_ni"] = df["toa_hi"]/limits["mu0"]
    
    if np.isin(["sza", "toa_hi", "global_integral"], columns).all():
        limits["ghi_possible_min"] = -4
        limits["ghi_possible_max"] = limits["toa_ni"] * 1.5 * np.power(limits["mu0"], 1.2) + 100
        limits["ghi_rare_min"] = -2
        limits["ghi_rare_max"] = limits["toa_ni"] * 1.2 * np.power(limits["mu0"], 1.2) + 50
        flags["ghi_possible_min"] = df["global_integral"] < limits["ghi_possible_min"]
        flags["ghi_possible_max"] = df["global_integral"] > limits["ghi_possible_max"]
        flags["ghi_rare_min"] = df["global_integral"] < limits["ghi_rare_min"]
        flags["ghi_rare_max"] = df["global_integral"] > limits["ghi_rare_max"]
    
    if np.isin(["sza", "toa_hi", "diffuse_integral"], columns).all():
        limits["dif_possible_min"] = -4
        limits["dif_possible_max"] = limits["toa_ni"] *0.95 * limits["mu0"]**1.2 + 50
        limits["dif_rare_min"] = -2
        limits["dif_rare_max"] = limits["toa_ni"] *0.75 * limits["mu0"]**1.2 + 30
        flags["dif_possible_min"] = df["diffuse_integral"] < limits["dif_possible_min"]
        flags["dif_possible_max"] = df["diffuse_integral"] > limits["dif_possible_max"]
        flags["dif_rare_min"] = df["diffuse_integral"] < limits["dif_rare_min"]
        flags["dif_rare_max"] = df["diffuse_integral"] > limits["dif_rare_max"]
    
    if np.isin(["sza", "toa_hi", "direct_normal_integral"], columns).all():
        limits["dni_possible_min"] = -4
        limits["dni_possible_max"] = limits["toa_ni"]
        limits["dni_rare_min"] = -2
        limits["dni_rare_max"] = limits["toa_ni"] * 0.95 * limits["mu0"]**0.2 + 10
        flags["dni_possible_min"] = df["direct_normal_integral"] < limits["dni_possible_min"]
        flags["dni_possible_max"] = df["direct_normal_integral"] > limits["dni_possible_max"]
        flags["dni_rare_min"] = df["direct_normal_integral"] < limits["dni_rare_min"]
        flags["dni_rare_max"] = df["direct_normal_integral"] > limits["dni_rare_max"]
    
    if np.isin(["diffuse_integral", "global_integral"], columns).all():
        limits["diffuse_ratio"] = df["diffuse_integral"]/df["global_integral"]
        flags["diffuse_ratio_sza_possible_max"] = limits["diffuse_ratio"] > 1
    
    if np.isin(["global_integral", "sza", "toa_hi"], columns).all():
        limits["ghi_toa"] = df["global_integral"]/df["toa_hi"]
    
    
    if np.isin(["direct_normal_integral", "global_integral", "sza", "toa_hi"], columns).all():
        limits["dni_toani"] = df["direct_normal_integral"]/limits["toa_ni"]
        flags["dni_toani_ghi_toa_possible_max"] = (limits["dni_toani"] > 0.95) | (limits["ghi_toa"] > 1.35) | ((limits["dni_toani"] < 0.95) & (limits["dni_toani"] > limits["ghi_toa"]))
    
    if np.isin(["diffuse_integral", "global_integral", "sza", "toa_hi"], columns).all():
        flags["diffuse_ratio_ghi_toa"] = (limits["diffuse_ratio"] > 1) | ((limits["ghi_toa"] > 0.6) & (limits["diffuse_ratio"] > 0.95))
    
    if ignore_nights and "sza" in columns:
        flags.loc[df["sza"] > np.radians(90)] = False
    
    return flags






def calculate_limits():
    """generates evenly spaced szas and calculates the bsrn limits, assuming 1 sed. used as a reference on graphs"""
    limits = pd.DataFrame()
    solar_cost = 844
    limits["SZA"] = np.radians(np.arange(0,100,1))
    limits["Sa"] = solar_cost#/np.power(df["sed"], 2)
    limits["toa_hi"] = limits["Sa"]*np.cos(limits["SZA"])
    
    limits["mu0"] = np.cos(limits["SZA"])
    
    limits["ghi_possible"] = limits["Sa"]*1.5*np.power(limits["mu0"], 1.2) + 100
    limits["ghi_rare"] = limits["Sa"]*1.2*np.power(limits["mu0"], 1.2) + 50
    
    limits["diff_possible"] = limits["Sa"]*0.95*np.power(limits["mu0"], 1.2) + 50
    limits["diff_rare"] = limits["Sa"]*0.75*np.power(limits["mu0"], 1.2) + 30
    
    limits["dni_possible"] = limits["Sa"]
    limits["dni_rare"] = limits["Sa"]*0.95*np.power(limits["mu0"], 0.2) + 10
    
    limits["diff/ghi_sza_comparison"] = 1
    
    
    limits["ghi_toa"] = (np.arange(0,100,1)/100)*1.5
    limits["ghi_toa"] = limits["ghi_toa"].clip(upper=1.35)
    limits["dni_toani"] = limits["ghi_toa"]
    limits["dni_toani"] = limits["dni_toani"].clip(upper=0.95)
    
    limits["ghi/toa"] = (np.arange(0,100,1)/100)*1.5
    limits["diff/ghi"] = 1.1
    limits.loc[limits["ghi/toa"] > 0.6, "diff/ghi"] = 0.95
    
    
    
    return limits