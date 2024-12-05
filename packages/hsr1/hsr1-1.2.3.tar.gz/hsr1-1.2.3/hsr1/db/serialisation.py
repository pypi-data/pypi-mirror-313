# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import pickle
import numpy as np
import array
import pandas as pd

class Serialisation:
    
    def __init__(self, method):
        self.method = method
    
    def __encode_array(self, data):
        """encodes a list of values using pythons array.array module"""
        # parameter can be 2d array or pd.Series of lists
        return [array.array("f", x).tobytes() for x in data]

    def __decode_array(self, binary):
        """decodes a byte array using pythons array.array module"""
        # parameter can be 2d array or pd.Series of lists
        decoded_data = []
        for data_array in binary:
            new_array = array.array("f") 
            new_array.frombytes(data_array)
            decoded_data.append(new_array.tolist())
        return decoded_data


    def __encode_pickle(self, data):
        """encodes a list of values using pythons pickle module"""
        # parameter can be 2d array or pd.Series of lists
        return [pickle.dumps(x) for x in data]

    def __decode_pickle(self, binary):
        """decodes a pickled object into a list of values"""
        # parameter can be 2d array or pd.Series of lists
        return [pickle.loads(x) for x in binary]


    def __encode_numpy(self, data):
        """encodes a list of values to bytes using numpy's to_bytes method"""
        # parameter can be 2d array or pd.Series of lists
        return [np.array(x).tobytes() for x in data]

    def __decode_numpy(self, binary):
        """decodes a bytearray to a numpyarray of values"""
        decoded_data = []
        for data_array in binary:
            decoded_data.append(np.frombuffer(data_array))
        return decoded_data
    
    
    def listify_and_serialise_numpy(df):
        """converts a dataframe with many columns into a series with a byte representation of an array of each row"""
        return pd.Series([np.array(x[1]).tobytes() for x in df.iterrows()], df.index)
        


    def encode_dataframe(self, spectral_data_df:pd.DataFrame):
        """encodes the spectral data of a dataframe using the instance variable method"""
        if self.method == "numpy":
            spectral_data_df["global_spectrum"] = self.__encode_numpy(spectral_data_df["global_spectrum"])
            spectral_data_df["diffuse_spectrum"] = self.__encode_numpy(spectral_data_df["diffuse_spectrum"]) 
        elif self.method == "pickle":
            spectral_data_df["global_spectrum"] = self.__encode_pickle(spectral_data_df["global_spectrum"])
            spectral_data_df["diffuse_spectrum"] = self.__encode_pickle(spectral_data_df["diffuse_spectrum"])        
        else:
            spectral_data_df["global_spectrum"] = self.__encode_array(spectral_data_df["global_spectrum"])
            spectral_data_df["diffuse_spectrum"] = self.__encode_array(spectral_data_df["diffuse_spectrum"]) 
        return spectral_data_df

    def decode_dataframe(self, spectral_data_df:pd.DataFrame, columns:[str]=["global_spectrum", "diffuse_spectrum"]):
        """decodes a subset of the spectral data in a dataframe
        params:
            spectral_data_df: the dataframe containing serialised spectral data
        columns:
            the specific columns in the dataframe that contain spectral data and are to be deserialised
            (saves time if e.g. only global spectrum is required)
        """
        if type(columns) == str:
            columns = [columns]
        
        if self.method == "numpy":
            for column in columns:
                spectral_data_df[column] = self.__decode_numpy(spectral_data_df[column])
        elif self.method == "pickle":
            for column in columns:
                spectral_data_df[column] = self.__decode_pickle(spectral_data_df[column])      
        else:
            for column in columns:
                spectral_data_df[column] = self.__decode_array(spectral_data_df[column])
        return spectral_data_df
