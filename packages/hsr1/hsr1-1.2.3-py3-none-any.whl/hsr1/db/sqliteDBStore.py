# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

import sqlite3
import pandas as pd
import numpy as np
import time
import os
import uuid

import hsr1

class SqliteDBStore():
    def __init__(self, driver):
        self.db_name = driver.db_name
        self.driver = driver
    
    
    
    def store(self, dfs, precalculate=True):
        """stores data to the database
        
        This function should usually only be used straight after reading data from a dataset of .zip files, 
        and you can pass the output of that straight into the dfs parameter of this function
        
        params:
            spectral_data, system_data, deployment_metadata: dataframes containing the data that will be stored to the database
        """
        print("storing to "+self.db_name)
        
        driver = self.driver
        
        ##### unpacking dfs from list
        spectral_data, system_data, deployment_metadata, *accessory_data_list = dfs
        accessory_data = accessory_data_list[0] if len(accessory_data_list) >= 1 else pd.DataFrame()
        
        ##### changes the datatypes of all the uuids to strings, as sqlite dosent support uuids
        spectral_data, system_data, deployment_metadata = self.__sqlite_change_types([spectral_data, system_data, deployment_metadata])
        deployment_metadata = deployment_metadata.reset_index(drop=True)
        
        if driver.exists():
            db_load = hsr1.db.SqliteDBLoad(self.db_name)
            deployment_metadata = self.match_deployment_ids(deployment_metadata, db_load)
            deployment_metadata = self.match_dataseries_ids(deployment_metadata, db_load)
        else:
            deployment_metadata["deployment_id"] = str(uuid.uuid1())
            deployment_metadata["dataseries_id"] = str(uuid.uuid1())
        
        spectral_data, system_data, accessory_data = self.__add_dataseries_ids(deployment_metadata["dataseries_id"].iloc[0], 
                                                                               spectral_data, system_data, accessory_data)
        
        
        ##### only add new data values
        if driver.exists():
            db_load = hsr1.db.SqliteDBLoad(self.db_name)
            table_names = db_load.load_table_names()
            if "deployment_metadata" in table_names.keys() and "spectral_data" in table_names.keys() and "system_data" in table_names.keys():
                ##### generate a dictionary that matches dataseries id to deployment id
                ##### key: dataseries_id value: deployment_id
                dataseries_deployment_ids = db_load.load(["dataseries_id", "deployment_id"])
                deployment_ids = {}
                for i in range(len(dataseries_deployment_ids)):
                    deployment_ids[dataseries_deployment_ids.loc[i, "dataseries_id"]] = dataseries_deployment_ids.loc[i, "deployment_id"]
                for i in range(len(deployment_metadata)):
                    new_dataseries_id = deployment_metadata.loc[i, "dataseries_id"]
                    new_deployment_id = deployment_metadata.loc[i, "deployment_id"]
                    if new_dataseries_id not in deployment_ids.keys():
                        deployment_ids[new_dataseries_id] = new_deployment_id
                
                spectral_data = self.__check_for_duplicates(spectral_data, "spectral_data", deployment_ids, db_load)
                system_data = self.__check_for_duplicates(system_data, "system_data", deployment_ids, db_load)
                
                
                ##### check accessory_data for duplicates
                if len(accessory_data) >= 1:
                    accessory_data = self.__check_for_duplicates(accessory_data, "accessory_data", deployment_ids, db_load)
                
                
                if len(spectral_data) == 0:
                    print("all timestamps are duplicated, no data is being added")
        
        if not os.path.exists(self.db_name):
            os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
        
        con = sqlite3.connect(self.db_name)
        
        normal_dfs = [spectral_data, system_data]
        normal_dfs_names = ["spectral_data", "system_data"]
        if len(accessory_data_list) >= 1:
            normal_dfs += [accessory_data]
            normal_dfs_names += ["accessory_data"]
            
        for i in range(len(normal_dfs)):
            if normal_dfs[i] is not None:
                self.store_dataframe(normal_dfs[i], normal_dfs_names[i])
        
        deployment_metadata.to_sql("deployment_metadata", con, if_exists="append", index=False)
        con.commit()
        con.close()
        
        if precalculate:
            mobile = False
            if deployment_metadata.loc[len(deployment_metadata)-1, "mobile"] == "1":
                mobile = True
            
            start_time = time.perf_counter()
            driver.add_precalculated_values(mobile=mobile, sample_ids_to_add=spectral_data["sample_id"].values, drop_existing=False)
            print("time to precalculate: ", time.perf_counter()-start_time)
    
    
    def store_raw(self, dfs, deployment_metadata):
        """stores raw data to the database
        
        params:
            dfs: tuple of dataframes, one dataframe per channel
            deployment_metadata: dataframe with one row, containing the deployment metadata for the dataseries being stored
        
        if no raw data already exists, creates a new table, "raw_data" which stores spectral data like in the spectral_data
        table, with each reading containing a blob that can be decoded to a spectral array
        """
        table_names = ["channel_"+str(i) for i in range(len(dfs))]
        
        big_df = pd.DataFrame()
        for i, df in enumerate(dfs):
            channel = pd.DataFrame(hsr1.db.Serialisation.listify_and_serialise_numpy(df), columns=[table_names[i]])
            channel = channel.reset_index()
            channel.columns = ["pc_time_end_measurement", table_names[i]]
            channel["pc_time_end_measurement"] = channel["pc_time_end_measurement"].astype(str)
            if len(big_df) == 0:
                big_df = channel
            else:
                big_df = big_df.merge(channel, on="pc_time_end_measurement")
        
        
        store = SqliteDBStore(self.driver)
        
        deployment_metadata = deployment_metadata.reset_index(drop=True)
        
        # TODO: more thorough check if db exists
        ##### checks if appending to a database or making new one, and if it already exists, checks to see if its the same deployment
        if self.driver.exists():
            db_load = self.driver.db_load
            store = SqliteDBStore(self.driver)
            deployment_metadata = store.match_deployment_ids(deployment_metadata, db_load)
            deployment_metadata = store.match_dataseries_ids(deployment_metadata, db_load)
        else:
            deployment_metadata["deployment_id"] = str(uuid.uuid1())
            deployment_metadata["dataseries_id"] = str(uuid.uuid1())
        
        store.store_dataframe(deployment_metadata, "deployment_metadata")
        store.store_dataframe(big_df, "raw_data") 
    
        
        

    def combine_database(self, new_db_name:str):
        """combines another database into the current database
        params:
            new_db_name: filepath to the database that will be merged into the current one
        
        """
        
        if not os.path.isfile(new_db_name):
            raise ValueError("databse to be merged: \""+new_db_name+" \" dosent exist")
        
        
        
        ##### avoid loading duplicates
        new_load = hsr1.db.SqliteDBLoad(new_db_name)
        
        new_metadata = new_load.load_metadata()
        metadata_to_store = new_metadata
        
        non_match_index_normal = None
        non_match_index_accessory = None
        
        existing_load = hsr1.db.SqliteDBLoad(self.db_name)
        
        new_tables = new_load.load_table_names()
        existing_tables = existing_load.load_table_names().keys()
        
        new_raw = False
        new_regular = False
        existing_raw = False
        existing_regular = False
        
        if "raw_data" in new_tables:
            new_raw = True
        if len(new_tables) >= 3:
            new_regular = True
        
        if "raw_data" in existing_tables:
            existing_raw = True
        if len(existing_tables) >= 3:
            existing_regular = True
        
        
        matched_metadata = self.match_deployment_ids(new_metadata, existing_load)
        metadata_to_store = matched_metadata
        
        
        if new_regular and existing_regular:
            ##### load all the dataseries_ids and deployment_ids from both tables and put into one dataframe
            existing_dataseries_deployment_ids = existing_load.load(["dataseries_id", "deployment_id"])
            new_dataseries_deployment_ids = matched_metadata[["dataseries_id", "deployment_id"]]
            dataseries_deployment_ids = pd.concat((existing_dataseries_deployment_ids, new_dataseries_deployment_ids))
            dataseries_deployment_ids = dataseries_deployment_ids.reset_index()
            
            deployment_ids = {}
            for i in range(len(dataseries_deployment_ids)):
                deployment_ids[dataseries_deployment_ids.loc[i, "dataseries_id"]] = dataseries_deployment_ids.loc[i, "deployment_id"]
            
            ##### dataframes with data from the database and data that is about to be added
            new_values = new_load.load(["pc_time_end_measurement", "dataseries_id"])
            
            existing_values = existing_load.load(["pc_time_end_measurement", "dataseries_id"])
            
            
            non_match_index_normal, num_dupes = self.find_matching_rows(existing_values, new_values, deployment_ids)
            print("skipping "+str(num_dupes)+" duplicated timestamps in spectral_data, system_data and precalculated_values")
            
            
            
            ##### load table names for existing and new table names
            existing_table_names = existing_load.load_table_names()
            new_table_names = new_load.load_table_names()
            ##### only need to check for dupes if both tables have accessory data
            if "accessory_data" in existing_table_names.keys() and "accessory_data" in new_table_names.keys():
                print("checking accessory_data for duplicate times")
                ##### dataframes with data from the database and data that is about to be added
                existing_values = existing_load.load_accessory(["pc_time_end_measurement", "dataseries_id"])
                new_values = new_load.load_accessory(["pc_time_end_measurement", "dataseries_id"])
                
                non_match_index_accessory, num_dupes = self.find_matching_rows(existing_values, new_values, deployment_ids)
                print("skipping "+str(num_dupes)+" duplicated timestamps in accessory_data")
            
            
            
            if len(non_match_index_normal) == 0 and non_match_index_accessory is not None and len(non_match_index_accessory) == 0:
                print("no data to merge: all times are duplicated")
            
            ##### sqlite ROWIDs are 1-based
            non_match_index_normal += 1
            non_match_index_normal = str(list(non_match_index_normal))
            non_match_index_normal = "(" + non_match_index_normal[1:]
            non_match_index_normal = non_match_index_normal[:-1] + ")"
            
            if non_match_index_accessory is not None:
                non_match_index_accessory += 1
                non_match_index_accessory = str(list(non_match_index_accessory))
                non_match_index_accessory = "(" + non_match_index_accessory[1:]
                non_match_index_accessory = non_match_index_accessory[:-1] + ")"
            
            
        
        
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("ATTACH \"" +new_db_name+"\"AS new_db")
        cur.execute("PRAGMA database_list;")
        
        new_load = hsr1.db.SqliteDBLoad(new_db_name)
        table_names = new_load.load_table_names()
        
        for table_name in table_names.keys():
            ##### TODO: remove?  \/
            sql = "PRAGMA table_info("+table_name+");"
            cur.execute(sql)
            # column_headers = [column[1] for column in cur.fetchall()]
            column_headers = table_names[table_name]
            column_string = ", ".join(column_headers)
            string = "CREATE TABLE IF NOT EXISTS "+table_name+"("+column_string+")"
            cur.execute(string)
            if table_name != "deployment_metadata":
                if non_match_index_normal is not None and table_name in ["spectral_data", "system_data", "precalculated_values"]:
                    cur.execute("INSERT INTO main."+table_name+" SELECT * FROM new_db."+table_name+" WHERE ROWID in "+non_match_index_normal)
                elif non_match_index_accessory is not None and table_name == "accessory_data":
                    cur.execute("INSERT INTO main."+table_name+" SELECT * FROM new_db."+table_name+" WHERE ROWID in "+non_match_index_accessory)
                else:
                    cur.execute("INSERT INTO main."+table_name+" SELECT * FROM new_db."+table_name)
        
        
        
        con.commit()
        con.close()
        self.store_dataframe(metadata_to_store, "deployment_metadata")

    
    def combine_database_folder(self, folder, delete=False):
        files = os.listdir(folder)
        databases = []
        for file in files:
            if file[-2:] == "db":
                databases.append(file)
        
        for db_name in databases:
            self.combine_database(folder+db_name)
            if delete:
                os.remove(folder+db_name)
            
    
    
    
    def drop_table(self, table_name:str):
        """drops a given table from the database
        
        params:
            table_name: the name of the table to be dropped
        """
        if not os.path.isfile(self.db_name):
            print("database does not exist")
            return None
        
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS "+table_name)
        con.commit()
        con.close()
    
    
    
    
    def match_deployment_ids(self, deployment_metadata:pd.DataFrame, db_load):
        """loads the deployment metadata from the database and checks if the deployment metadata being stored and matches the deployment ids if it is
        params:
            deployment_metadata: the new dataframe being added to the database
            db_load: a db_load object that can load from the database
        returns:
            deployment_metadata: the original dataframe with updated deployment_ids if required
        
        iterates through each row of deployment data that will be added, and checks it against each row of deployment_metadata already in the database,
        if the deployment data(dosent check dataseries data) matches, copies the preexisting deployment_id to the new data
        this allows grouping all data from a specific deployment, when the deployment id isnt included in the deployment's config file'
        """
        # TODO: get this from deployment file
        # subset of columns that refer to the deployment, rather than the dataseries
        deployment_columns = ["data_structure_id", 
                              "deployment_description", 
                              "sensor_type", 
                              "sensor_id", 
                              "camera_id", 
                              "owner_contact", 
                              "operator_contact", 
                              "license", 
                              "license_reference",
                              "deployment_id"]
        
        deployment_metadata = self.__match_deployment_metadata_ids(deployment_metadata, deployment_columns, "deployment_id", db_load)
        
        return deployment_metadata

    
    def match_dataseries_ids(self, deployment_metadata:pd.DataFrame, db_load):
        dataseries_columns = ["mobile",
                              "processing_level",
                              "timezone",
                              "location_name",
                              "default_latitude",
                              "default_longitude",
                              "default_elevation",
                              "dataseries_id",
                              "platform_id",
                              "software_id",
                              "calibration_time",
                              "calibration_comment",
                              "camera_calibration_file",
                              "spectrometer_calibration_file",
                              "start_time",
                              "integration_time",
                              "gain",
                              "hdr",
                              "spectrometer_sampling_period",
                              "spectrometer_average_period",
                              "spectrometer_burst_number",
                              "wavelengths",
                              "aux_sampling_period",
                              "aux_average_period"]
        
        deployment_metadata = self.__match_deployment_metadata_ids(deployment_metadata, dataseries_columns, "dataseries_id", db_load)
        
        return deployment_metadata
    
    def store_dataframe(self, df:pd.DataFrame, table_name:str):
        """stores one dataframe to a table in the database
        
        params:
            df: the dataframe being stored
            table_name: the name of the table it will be stored to
        """
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        question_marks = ["?" for i in range(len(df.columns))]
        question_marks_string = ", ".join(question_marks)
        
        column_string = ", ".join(df.columns.to_list())
        
        create_table_sql = "CREATE TABLE IF NOT EXISTS "+table_name+"("+column_string+")"
        cur.execute(create_table_sql)
        
        sql = "INSERT INTO "+table_name+" VALUES("+question_marks_string+")"
        cur.executemany(sql, df.values)
        
        con.commit()
        con.close()
    
    
    def __match_deployment_metadata_ids(self, df, columns, id_type:str, db_load):
        try:
            existing_deployment_metadata = db_load.load_metadata(columns)
        except KeyError:
            print("no deployment_metadata found in existing table")
            return df
        new_df = df[columns]
        
        # loops through each row of new deployment data (can be multiple, e.g: copying across databases)
        #   and through checks it against each row of existing deployment data from the database
        #   dosent check deployment_id column because that will be different
        for i, deployment in enumerate(new_df.drop(id_type, axis=1).iterrows()):
            found = False
            for j, existing_deployment in enumerate(existing_deployment_metadata.drop(id_type, axis=1).iterrows()):
                if deployment[1].equals(existing_deployment[1]):
                    found = True
                    print("deployment metadata matches, using same deployment id")
                    df.loc[i,id_type] = existing_deployment_metadata.loc[j,id_type]
                    break
            if not found:
                print("no deployment id found, generating new one")
                df.loc[i,id_type] = str(uuid.uuid1())
        
        return df
    
    def __add_dataseries_ids(self, dataseries_id, spectral_data, system_data, accessory_data=None):
        """adds a given dataseries id to given dataframes"""
        if spectral_data is not None:
            spectral_data["dataseries_id"] = dataseries_id
        if system_data is not None:
            system_data["dataseries_id"] = dataseries_id
        if accessory_data is not None and len(accessory_data) > 0:
            accessory_data["dataseries_id"] = dataseries_id
            
        return spectral_data, system_data, accessory_data
    
    def __sqlite_change_types(self, dataframes:[pd.DataFrame]) -> [pd.DataFrame()]:
        """change the type of all the uuids to strings
        params:
            dataframes: list of dataframes to be converted
                [spectral_data, system_data, deployment_metadata]
        returns:
            dataframes: list of converted dataframes, same format as parameter
        """
        
        uuid_columns = ["sample_id", "dataseries_id", "deployment_id"]
        
        output_dataframes = []
        for df in dataframes:
            if df is None:
                output_dataframes.append(None)
            else:
                for column in uuid_columns:
                    if column in df.columns:
                        df[column] = df[column].astype(str)
                output_dataframes.append(df)
        return output_dataframes
    
    
    def __check_for_duplicates(self, data, table_name, deployment_ids, db_load):
        """
        params:
            deployment_ids: a dictionary that can convert dataseries_ids
              to deployment_ids. dataseries_ids are the keys and deployment_ids are the values.
        """
        print("checking for duplicates")
        existing_values = None
        ##### dataframes with data from the database and data that is about to be added
        try:
            existing_values = db_load.load(["pc_time_end_measurement", "dataseries_id"], table=table_name)
        except ValueError:
            ##### if there is no data in the database for this table, no need to check for dupes, just return original data
            return data
        
        if data is None:
            return None
        
        new_values = data[["pc_time_end_measurement", "dataseries_id"]].copy()
        new_values["pc_time_end_measurement"] = pd.to_datetime(new_values["pc_time_end_measurement"]).dt.tz_convert("+00:00")
        
        existing_values["pc_time_end_measurement"] = pd.to_datetime(existing_values["pc_time_end_measurement"]).dt.tz_convert(None)
        new_values["pc_time_end_measurement"] = pd.to_datetime(new_values["pc_time_end_measurement"]).dt.tz_convert(None)
        
        
        ##### find index of all non-duplicated values
        non_match_index, num_dupes = self.find_matching_rows(existing_values, new_values, deployment_ids)
        print("skipping "+str(num_dupes)+" duplicated timestamps in "+table_name)        
        
        ##### filter for all valid readings
        data = data.iloc[non_match_index]
        
        return data
    
    def find_matching_rows(self, existing, new, deployment_ids):
        ##### replace dataseries_id with deployment id and rename
        existing = existing.replace(deployment_ids).rename(columns={"dataseries_id":"deployment_id"})
        new = new.replace(deployment_ids).rename(columns={"dataseries_id":"deployment_id"})
        
        ##### selecting for same deployment
        deployment_id = new.loc[1, "deployment_id"]
        id_existing = existing.loc[existing["deployment_id"] == deployment_id, "pc_time_end_measurement"]
        id_new = new.loc[new["deployment_id"] == deployment_id, "pc_time_end_measurement"]
        
        if len(id_existing) == 0:
            raise ValueError("existing data has a different deployment_id to the new data, not merging")
        
        id_existing = pd.to_datetime(id_existing)
        id_new = pd.to_datetime(id_new)
        
        
        existing_limits = (id_existing.iloc[0],
                           id_existing.iloc[len(id_existing)-1])
        new_limits = (id_new.iloc[0],
                      id_new.iloc[len(id_new)-1])
        
        existing_intersection = np.logical_and(id_existing >= new_limits[0],
                                               id_existing <= new_limits[1])
        new_intersection = np.logical_and(id_new >= existing_limits[0],
                                          id_new <= existing_limits[1])
        
        trimmed_existing_values = id_existing.loc[existing_intersection].reset_index(drop=True)
        trimmed_new_values = id_new.loc[new_intersection].reset_index(drop=True)
        
        matches = np.isin(trimmed_new_values, trimmed_existing_values)
        
        invalid = new_intersection
        invalid[new_intersection] = matches
        
        
        non_match_index = id_new.index[np.logical_not(invalid)]
        
        num_dupes = sum(matches)
        
        return non_match_index, num_dupes
    
    