# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import time

import uuid

import pandas as pd
import numpy as np


from hsr1.utils.config import Config

class ReformatData():
    def reformat_data(self, dataframes:[pd.DataFrame], deployment_metadata_file_path:str, gps_type=None):
        """combines various methods to reformat all the data necessary for storing to the database
        params:
            dataframes: list of 6 dataframes: [ed, eds, summary, hdr, ind_ch, gps]
            deployment_metadata_file_path: path to the deployment metadata .ini file
            gps_type: the type of gps file, either "gps", or accessory"
        returns:
            spectral_data, precalculated_values, system_data, deployment_metadata
        """
        print("reformatting data")
        deployment_metadata = self.reformat_deployment_metadata(deployment_metadata_file_path)
        spectral_data = self.reformat_spectral_data(dataframes[:3])
        system_data = None
        accessory_data = None
        
        if dataframes[4] is None:       # for datasets with no GPS, create a dummy from default values
            print("No GPS data found")
            system_data=None
        else:
            gps_data = dataframes[4]
            if gps_type is None:        # check gps_type is set correctly
                columns = gps_data.columns
                if len(columns) > 12:
                    print("no gps_type passed, assuming accessory")
                    gps_type = "accessory"
                else:
                    print("no gps_type passed, assuming gps")
                    gps_type = "gps"
            if gps_type == "accessory":
                accessory_data = self.reformat_accessory_data(gps_data)

            system_data = self.reformat_system_data(gps_data, gps_type, accessory_data, spectral_data.index)
            
            
        if system_data is not None:
            if deployment_metadata["mobile"].iloc[0]:
                aux_average_period = int(deployment_metadata["aux_average_period"].iloc[0])
                ##### tolerance in in ns, convert s to ns
                system_data = self.match_sample_ids(spectral_data, system_data, "sample_id", tolerance=aux_average_period*10**9)
            else:
                system_data = self.match_sample_ids(spectral_data, system_data, "sample_id")
            
            ##### fills in all nan sample_id values as that will cause a crash
            nan_readings = system_data["sample_id"].isna()
            uuids = [uuid.uuid1() for i in range(sum(nan_readings))]
            system_data.loc[nan_readings, "sample_id"] = uuids
        
        spectral_data = self.reset_index(spectral_data, "pc_time_end_measurement")
        
        tz_string = deployment_metadata.iloc[0]["timezone"]
        timezone, timedelta = self.calculate_timezone(tz_string)
        
        
        default_location = [deployment_metadata["default_longitude"].iloc[0],  
                            deployment_metadata["default_latitude"].iloc[0],
                            deployment_metadata["default_elevation"].iloc[0]]
        for i in range(len(default_location)):
            if default_location[i] == "''":
                default_location[i] = np.nan
            default_location[i] = float(default_location[i])
        
        if system_data is not None:
            invalid_gps = system_data["gps_status"].str.slice(stop=1) == "V"
            system_data.loc[invalid_gps, "gps_longitude"] = default_location[0]
            system_data.loc[invalid_gps, "gps_latitude"] = default_location[1]
            system_data.loc[invalid_gps, "gps_altitude"] = default_location[2]
        
        dfs = [spectral_data, system_data, accessory_data] if gps_type == "accessory" else [spectral_data, system_data]
        
        for df in dfs:
            if df is not None:
                # df["pc_time_end_measurement"] = (pd.to_datetime(df["pc_time_end_measurement"])+timedelta).astype(str)
                df["pc_time_end_measurement"] = df["pc_time_end_measurement"].astype(str)+timezone
        
        dfs = [spectral_data, system_data, deployment_metadata, accessory_data] if gps_type == "accessory" else [spectral_data, system_data, deployment_metadata]
        return tuple(dfs)
    

    def reformat_deployment_metadata(self, file_path:str) -> pd.DataFrame:
        """reformats the deployment metadata found in an .ini file
        params:
            file_path: the location of the deployment metadata .ini file
        returns:
            df: the database version of the deployment metadata file
        
        storing this as a one line dataframe is very inneficient, but the sizes are so small,
            it doesent have an impact on performance, so maybe its best to keep it consistent with the other tables
        """
        print("reformatting deployment metadata")
        config_reader = Config(file_path)
        params = config_reader.read_section("deployment") | config_reader.read_section("dataseries")
        
        if not "mobile" in params.keys():
            if params["default_longitude"] == "''" or params["default_latitude"] == "''":
                params["mobile"] = True
            else:
                params["mobile"] = False
        
        if not "location_name" in params.keys():
            params["location_name"] = ""
        
        self.dataseries_id = params["dataseries_id"]
        df = pd.DataFrame.from_records(params, index = ["1"])
        
        return df
    
    
    def reformat_spectral_data(self, dataframes:[pd.DataFrame]) -> pd.DataFrame:
        """reformats spectral data from the format in the txt files to the database format
        params:
            dataframes: list of dataframes, [ed, eds, summary]
        returns:
            spectral_data: dataframe of same structure as database
        """
        print("reformatting spectral data")
        ed:pd.DataFrame = dataframes[0]
        eds:pd.DataFrame = dataframes[1]
        summary:pd.DataFrame = dataframes[2]
        
        # round times to the nearest minute
        # ed = self.__round_times(ed, "min")
        # eds = self.__round_times(eds, "min")
        # summary = self.__round_times(summary, "min")
        
        # select all the rows in the dataframe that are not duplicates
        ed = ed[~ed.index.duplicated()]
        eds = eds[~eds.index.duplicated()]
        summary = summary[~summary.index.duplicated()]
        
        ed = self.listify(ed)
        eds = self.listify(eds)
        
        
        spectral_data = pd.DataFrame()
        
        spectral_data["global_spectrum"] = ed
        spectral_data["diffuse_spectrum"] = eds
        spectral_data = spectral_data.merge(summary, left_index=True, right_index=True)
        
        spectral_data["dataseries_id"] = ""
        
        # spectral_data = spectral_data.reset_index()
        spectral_data = spectral_data.rename(columns={#"index":"pc_time_end_measurement",
                                                      "Total W": "global_integral",
                                                      "Diffuse W": "diffuse_integral",
                                                      "Total Molar": "global_molar",
                                                      "Diffuse Molar": "diffuse_molar",
                                                      "Temp": "camera_temp"})
        
        # generate a unique sample ID for each row that will be matched to the system data table
        spectral_data["sample_id"] = [uuid.uuid1() for i in range(len(spectral_data))]
        
        # reposition the data to be in the correct order
        spectral_data = spectral_data[["sample_id",
                                       "dataseries_id", 
                                       "global_spectrum", 
                                       "diffuse_spectrum", 
                                       "global_integral", 
                                       "diffuse_integral", 
                                       "global_molar", 
                                       "diffuse_molar", 
                                       "camera_temp"]]
        return spectral_data
        
        
    
    def reformat_system_data(self, gps:pd.DataFrame, gps_type:str, accessory_data:pd.DataFrame=None, spectral_timestamps:pd.Series=None) -> pd.DataFrame:
        """reformats data from the gps text file to the database format
        params:
            gps: dataframe containing gps data
            gps_type: type of gps file used, "gps", or "accessory"
        returns:
            gps: reformatted dataframe in the correct format for the database
        """
        if gps_type == "gps":
            gps = self.reformat_system_data_gps(gps)
        elif gps_type == "accessory":
            # gps = self.reformat_system_data_accessory(gps)
            if accessory_data is None:
                raise ValueError("if gps_type is accessory, accessory_data must be passed")
            gps = self.reformat_system_data_reformatted_accessory(accessory_data, spectral_timestamps)
        else:
            print("gps_type not recognised")
        
        ##### reorder gps columns so it is consistent
        if "pc_time_end_measurement" in gps.columns:
            gps = gps.set_index("pc_time_end_measurement")
        gps = gps[["gps_time",
                   "gps_status",
                   "gps_latitude",
                   "gps_longitude",
                   "gps_altitude",
                   "pressure",
                   "baro_temp",
                   "rh",
                   "rh_temp",
                   "dataseries_id"]]
        return gps
    
    def reformat_system_data_gps(self, gps:pd.DataFrame) -> pd.DataFrame:
        """reformats data from the gps text file to the database format
        params:
            gps: dataframe containing gps data
        returns:
            gps: reformatted dataframe in the correct format for the database
        """
        print("reformatting gps data")
        
        if len(gps.columns) > 12:
            raise ValueError("trying to reformat gps data, too many columns in dataframe")
        
        gps = self.__round_times(gps, "min")
        
        gps = gps.rename(columns={"pc_time": "pc_time_end_measurement",
                                  "GPS Time": "gps_time",
                                  "Status": "gps_status",
                                  "Latitude": "gps_latitude",
                                  "Longitude": "gps_longitude",
                                  "Altitude": "gps_altitude",
                                  "Pressure": "pressure",
                                  "BaroTemp": "baro_temp",
                                  "RH": "rh",
                                  "RHTemp": "rh_temp"})
        
        gps = gps.drop(["HDOP", "TP0", "TP1"], axis = 1)
        
        gps["dataseries_id"] = ""
        
        return gps
    
    # def reformat_system_data_accessory(self, gps):
    #     """reformats data from the accessory text file to the database format
    #     params:
    #         gps: dataframe containing gps data
    #     returns:
    #         gps: reformatted dataframe in the correct format for the database
    #     """
    #     print("reformatting accessory data")
        
    #     if len(gps.columns) <= 12:
    #         raise ValueError("trying to reformat accessory data, too few columns in dataframe")
        
    #     gps = gps.drop(gps[gps["0 TimeYYYY"] == 0].index)
        
    #     gps = self.__round_times(gps, "min")
        
    #     ##### merge the gps time columns into one time column
    #     gps_date_cols = ["9 GPSYYYY", "10 GPSMonth", "11 GPSDay"]
    #     gps_time_cols = ["12 GPSHour", "13 GPSMin", "14 GPSSec"]
    #     gps[gps_date_cols] =  gps[gps_date_cols].astype(int).astype(str)
    #     gps[gps_time_cols] =  gps[gps_time_cols].astype(int).astype(str)
        
    #     ##### this line is the (speed) problem \/
    #     gps["gps_time"] = gps[gps_date_cols].agg("-".join, axis=1) + " " + gps[gps_time_cols].agg(":".join, axis=1)

    #     ##### where gps cuts out, use pc_time to stop errors
    #     gps["gps_time"] = gps["gps_time"].where(gps["gps_time"].str.slice(0,0) == "0", gps.index)
        
    #     gps["gps_time"] = pd.to_datetime(gps["gps_time"])
        
    #     gps = self.reset_index(gps, "pc_time_end_measurement")
        
    #     gps["gps_status"] = ""
    #     gps.loc[gps["18 GPSAge"] < 10, "gps_status"] = "A"
        
    #     new_gps = gps[["pc_time_end_measurement", "gps_time", "gps_status", "15 Latitude", "16 Longitude", "17 Altitude", "36 Pressure", "34 T-Baro", "35 RH%", "33 T-RH"]].copy()
        
        
    #     new_gps = new_gps.rename(columns={"15 Latitude":"gps_latitude",
    #                               "16 Longitude":"gps_longitude",
    #                               "17 Altitude":"gps_altitude",
    #                               "36 Pressure":"pressure",
    #                               "34 T-Baro":"baro_temp",
    #                               "35 RH%":"rh",
    #                               "33 T-RH":"rh_temp"})
        
    #     new_gps = new_gps.reset_index(drop=True)
        
        
    #     ##### averages rows to the nearest minute
    #     new_gps["pc_time_end_measurement"] = new_gps["pc_time_end_measurement"].round("min")
    #     ##### to get time from the end of the period:
    #     merged_gps = new_gps.groupby(new_gps["pc_time_end_measurement"])[["pc_time_end_measurement", "gps_time", "gps_latitude", "gps_longitude", "gps_altitude", "pressure", "baro_temp", "rh", "rh_temp"]].mean()
    #     # TODO: how to merge gps status(first? keep worst?)
    #     merged_gps["gps_status"] = new_gps[["pc_time_end_measurement", "gps_status"]].groupby(new_gps["pc_time_end_measurement"]).first()["gps_status"]
        
    #     merged_gps["dataseries_id"] = ""
        
    #     merged_gps["gps_time"] = merged_gps["gps_time"].astype(str)
        
    #     merged_gps = merged_gps.drop("pc_time_end_measurement", axis=1)
        
        
        
    #     return merged_gps
    
    
    def reformat_system_data_reformatted_accessory(self, accessory:pd.DataFrame, spectral_timestamps:pd.Series=None, spectral_sample_ids:pd.Series=None, aux_average_period=60):
        """averages accessory data to the same time period as spectral data,
        this will be stored in the system_data table
        
        params:
            accesssory: the raw accessory data.
            spectral_timestamps: all the timestamps where there are spectral readings.
        returns:
            averaged_system_data: ddataframe of the reformatted data.
        """
        print("reformatting accessory data")
        ##### filter out all the readings that arent within the aux_average_period, as those shouldnt be averaged
        
        
        system_data = accessory[["pc_time_end_measurement",
                               "gps_time",
                               "Latitude",
                               "Longitude",
                               "Altitude",
                               "Pressure",
                               "T_Baro",
                               "RH",
                               "T_RH"]]
        system_data = system_data.rename(columns = {"Latitude":"gps_latitude",
                                                    "Longitude":"gps_longitude",
                                                    "Altitude":"gps_altitude",
                                                    "Pressure":"pressure",
                                                    "T_Baro":"baro_temp",
                                                    "RH":"rh",
                                                    "T_RH":"rh_temp"})
        
        system_data["gps_status"] = "V"
        system_data.loc[accessory["GPSAge"] < 10, "gps_status"] = "A"
        
        
        if spectral_timestamps is None:
            print("no spectral_timestamps provided to average to, not averaging system_data")
            return system_data
        
        system_timestamps = pd.to_datetime(system_data["pc_time_end_measurement"]).astype("int64").values
        spectral_timestamps_int = pd.to_datetime(spectral_timestamps).astype("int64").values
        
        
        # #### split into chunks, one per day? limits the n^2edness
        # #### have to make sure no data is lost at the splits
        # start_time = time.perf_counter()
        # time_until_next_spectral = (spectral_timestamps_int[:, np.newaxis] - system_timestamps).astype(float)
        # time_until_next_spectral = time_until_next_spectral/10**9
        # time_until_next_spectral[time_until_next_spectral < 0] = np.inf
        # time_until_closest_spectral = np.min(time_until_next_spectral, axis=0)
        # print("big array time: " +str(time.perf_counter()-start_time))
        
        
        
        # start_time = time.perf_counter()
        # spectral_timestamps_int_editable = spectral_timestamps_int
        # time_until_closest_spectral = np.full(len(system_timestamps), np.inf)
        # ##### loops through every value which system_timestamps is less than the max spectral timestamp
        # #####   to ignore values that will never be averaged into spectral_timestamp and will cause errors
        # for i in range(np.sum(system_timestamps<=np.max(spectral_timestamps_int))):
        #     system_timestamp = system_timestamps[i]
            
        #     # spectral_timestamps_int_editable = spectral_timestamps_int_editable[spectral_timestamps_int_editable>=system_timestamp]
        #     # time_until_next_spectral = spectral_timestamps_int_editable[0]-system_timestamp
            
        #     ##### arg of first value that is greater than current. this will be the closest
        #     greater_than_current_pointer = np.argmax(spectral_timestamps_int_editable>=system_timestamp)
            
        #     #####convert to elementwise subraction after?
        #     time_until_next_spectral = spectral_timestamps_int_editable[greater_than_current_pointer]-system_timestamp
        #     time_until_closest_spectral[i] = time_until_next_spectral
        
        # time_until_closest_spectral = np.array(time_until_closest_spectral)/10**9
        # print("for loop time: " +str(time.perf_counter()-start_time))
        
        
        # within_average_period = time_until_closest_spectral < float(aux_average_period)
        

        # system_data = system_data[within_average_period].reset_index(drop=True)
        # system_timestamps = system_timestamps[within_average_period]
        
        str_cols = ["pc_time_end_measurement", "gps_time", "gps_status"]
        float_cols = ~np.isin(system_data.columns, str_cols)
        floats = system_data.loc[:, float_cols].astype(float)
        system_data.loc[:, float_cols] = floats
        
        
        agg_dict = {col:"last" for col in system_data.columns}
        
        for col in ["gps_latitude", "gps_longitude", "gps_altitude", "pressure", "baro_temp", "rh", "rh_temp"]:
            agg_dict[col] = "mean"
        
        averaged_system_data = system_data.groupby(spectral_timestamps_int[np.clip(np.digitize(system_timestamps, spectral_timestamps_int, right=True), 0, len(spectral_timestamps)-1)])#.agg(agg_dict)
        averaged_system_data = averaged_system_data.agg(agg_dict)
        
        int_to_timestamp = pd.DataFrame(index=spectral_timestamps_int)
        int_to_timestamp["pc_time_end_measurement"] = spectral_timestamps.values
        averaged_system_data["pc_time_end_measurement"] = int_to_timestamp.loc[averaged_system_data.index]
        
        ##### filter out readings that are more than aux_average_period from the previous reading.
        #####   filters the reading after big jumps
        time_since_last_reading = np.diff(pd.to_datetime(averaged_system_data["pc_time_end_measurement"]).astype("int64").values/10**9)
        normal_gaps = time_since_last_reading <= aux_average_period
        normal_gaps = np.array([1] + list(normal_gaps)).astype(bool)
        averaged_system_data = averaged_system_data.loc[normal_gaps, :]
        
        averaged_system_data = averaged_system_data.reset_index(drop=True)
        
        averaged_system_data[str_cols] = averaged_system_data[str_cols].astype(str)
        
        
        averaged_system_data["dataseries_id"] = ""
        
        return averaged_system_data
    
    
    def reformat_accessory_data(self, accessory):
        """changes column headings on accessory data to prepare it for storing to the database
        params:
            accessory: df containing the accessory data
        returns:
            accessory: reformatted df containing accessory data
        
        note: there is a wierd bug with the tara dataset where halfway through, the name of column 51
              from "51 Control flags" to "51 Control flags2"
        """
        
        ##### merging control flags with control flags2
        if "51 Control flags2" in accessory.columns and "51 Control flags" in accessory.columns:
            accessory["51 Control flags2"] = accessory["51 Control flags2"].fillna(accessory["51 Control flags"])
            accessory = accessory.drop("51 Control flags", axis="columns")
        elif "51 Control flags" in accessory.columns:
            accessory = accessory.rename(columns={"51 Control flags":"51 Control flags2"})
            
        columns = accessory.columns
        new_columns = ["51 Control flags2" if i == "51 Control flags" else i for i in columns]
        new_columns = [column[column.find(" ")+1:] for column in new_columns]
        
        ##### sql column headers can only be letters or underscores, so replace invalid characters with underscores
        ##### also cant start with a number, so preface those columns with an underscore
        for i, col in enumerate(new_columns):
            new_columns[i] = new_columns[i].replace("-", "_")
            new_columns[i] = new_columns[i].replace(" ", "_")
            new_columns[i] = new_columns[i].replace("%", "")
            if col[0].isnumeric():
                new_columns[i] = "_"+col
            
        accessory = accessory.rename(columns=dict(zip(columns, new_columns)))
        ##### merge the gps time columns into one time column
        gps_date_cols = ["GPSYYYY", "GPSMonth", "GPSDay"]
        gps_time_cols = ["GPSHour", "GPSMin", "GPSSec"]
        accessory = self.__merge_date_cols(accessory, "gps_time", gps_date_cols, gps_time_cols)
        accessory = accessory.drop(gps_date_cols + gps_time_cols, axis="columns")
        
        pc_date_cols = ["TimeYYYY", "Month", "Day"]
        pc_time_cols = ["Hour", "Minute", "Second"]
        accessory = self.__merge_date_cols(accessory, "cpu_time", pc_date_cols, pc_time_cols, "milliseconds", "Timezone")
        accessory = accessory.drop(pc_date_cols + pc_time_cols + ["milliseconds", "Timezone"], axis="columns")
        
        accessory = self.reset_index(accessory, "pc_time_end_measurement")
        
        return accessory
    
    
    def calculate_timezone(self, timezone):
        ##### reads timezone data from ini file and converts utc time to tzaware timestamp, stored as string
        if timezone[0] != "+" and timezone[0] != "-":
            timezone = "+"+timezone
        timezone_components = timezone.split(":")
        
        mins = 0
        if len(timezone_components) == 2:
            mins = abs(int(timezone_components[0]))*60 + abs(int(timezone_components[1]))
        else:
            mins = abs(int(timezone))*60
        
        if timezone[0] == "-":
            mins = -mins
            
        timedelta = pd.Timedelta(mins, "minutes")
        return timezone, timedelta
    
    
    def __merge_date_cols(self, df, name, date_cols, time_cols, millisecond="", timezone=""):
        df[date_cols] = df[date_cols].astype(int).astype(str)
        df[time_cols] = df[time_cols].astype(int).astype(str)
        
        ##### zero pad dates and times
        for date_col in date_cols:
            df.loc[df[date_col].str.len() == 1, date_col] = "0"+df.loc[df[date_col].str.len() == 1, date_col]
        for time_col in time_cols:
            df.loc[df[time_col].str.len() == 1, time_col] = "0"+df.loc[df[time_col].str.len() == 1, time_col]
        
        timezones = milliseconds = []
        if millisecond == "":
            milliseconds = ""
        else:
            milliseconds = df[millisecond].astype(int).astype(str)
        
        if timezone == "":
            timezones = ""
        else:
            timezones =  df[timezone].astype(int).astype(str)
        
        
        ##### these lines are the (speed) problem \/
        dates = df[date_cols].agg("-".join, axis=1)
        times = df[time_cols].agg(":".join, axis=1)
        
        ##### to avoid trailing .
        if type(milliseconds) is str:
            df[name] = dates + " " + times + milliseconds + timezones
        else:
            df[name] = dates + " " + times + "." + milliseconds + timezones
        
        return df
    
    def __round_times(self, df:pd.DataFrame, frequency:str) -> pd.DataFrame:
        """rounds the index of a dataframe to the nearest value, as passed
        params:
            df: dataframe to be rounded
            frequency: what to round the database to ('min', 'hour' etc)
            https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases
        returns:
            df: the rounded dataframe
        """
        df.index = df.index.round(frequency)
        return df
    
    def match_sample_ids(self, source:pd.DataFrame, to_be_matched:pd.DataFrame, column:str, tolerance=None) -> pd.DataFrame:
        """matches the sample ids from a dataframe with sample ids(or other columns) to one without, where they share a timestamp
        params:
            source: dataframe that already has ids
            to_be_matched: dataframe that will take the id from source where timestamps match
            column: the column that will be transferred from source, usually sample_id
            tolerance: if there isnt a perfect match, how far either side to look (ns)
        returns: to_be_matched: the dataframe with the matched ids added
        """
        
        match_df = pd.DataFrame(np.array([source.index, source[column]]).T, columns=["pc_time_end_measurement", column])
        to_be_matched = to_be_matched.copy()
        
        match_df["pc_time_end_measurement"] = pd.to_datetime(match_df["pc_time_end_measurement"])
        
        to_be_matched = self.reset_index(to_be_matched, "pc_time_end_measurement")
        to_be_matched["pc_time_end_measurement"] = pd.to_datetime(to_be_matched["pc_time_end_measurement"])
        
        
        to_be_matched["pc_time_end_measurement"] = to_be_matched["pc_time_end_measurement"].astype("int64")
        match_df["pc_time_end_measurement"] = match_df["pc_time_end_measurement"].astype("int64")
        
        
        merged_df = pd.merge_asof(to_be_matched, match_df, on="pc_time_end_measurement", direction="nearest", tolerance=tolerance)
        
        to_be_matched["sample_id"] = merged_df["sample_id"]
        
        to_be_matched["pc_time_end_measurement"] = pd.to_datetime(to_be_matched["pc_time_end_measurement"])
        
        return to_be_matched
    
    def listify(self, df):
        """converts a dataframe with many columns into a series with an array representing each row"""
        return pd.Series([np.array(x[1]) for x in df.iterrows()], df.index)
    
    def reset_index(self, df, column_name):
        """copies the index into a column with the name column_name and sets the index to integers
        params:
            df: dataframe that will be changed
            column_name: new name for the old index
        returns:
            df: dataframe with the new column
        
        this method can be replaced with pandas' reset_index names= parameter, but that's new in pandas v1.4,
        so ive added this for backwards compatibility
        """
        df = df.reset_index()
        columns = df.columns.to_list()
        columns[0]=column_name
        df.columns = columns
        return df
        