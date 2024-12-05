# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import os
import time

import pandas as pd
import numpy as np
import sqlite3

from hsr1.db import Serialisation
from hsr1.utils import ReformatData as reformat

class SqliteDBLoad():
    """Handles all the loading from the database"""
    def __init__(self, db_name:str):
        """
        params:
            db_name: the name of the db you are loading from
        """
        if os.path.isfile(db_name):
            self.exists = True
        else:
            self.exists = False
        self.db_name = db_name
    
    
    
    
    def load_table_names(self) -> dict:
        """return a dictionary of all the table names and their corresponding column names"""
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        ##### get all the table names
        sql = "SELECT name FROM sqlite_schema WHERE type='table'"
        cur.execute(sql)
        table_names = [table[0] for table in cur.fetchall()]
        
        ##### get all the column headers for each table
        column_headers = {}
        for table in table_names:
            sql = "PRAGMA table_info("+table+");"
            cur.execute(sql)
            column_headers[table] = [column[1] for column in cur.fetchall()]
        
        con.close()
        return column_headers
    
    
    def load(self, columns:[str]=[], 
             table:str=None,
             start_time:str=None, 
             end_time:str=None,
             condition:str="",
             raise_on_missing:bool=True,
             sort:bool=True,
             deserialise:bool=True,
             timezone:str="+00:00",
             **kwargs,
             ) -> pd.DataFrame:
        ##### TODO: fix docstring
        """loads data from the database
        params:
            columns: list of column names to extract from database, if empty, returns all
            table: which table to load data from. Not necessary but can be useful to specify when multiple tables have the same column
            start_time, end_time: for only selecting data within a time period
                format: ISO-8601("2023-05-23 00:00:00")
                if you dont put in a full datetime, it will assume first timestamp,
                    e.g: 2023-05-23 will be read as 2023-05-23 00:00:00.
                    therefore, start_time is inclusive, end time is not
            condition: sql that comes after the WHERE in an sql statement.
                e.g: gobal_integral>50
                if you want even more control, use load_sql
            raise_on_missing: how to handle when columns arent found, raise or just load if possible
            sort: sorts the results from the database
            deserialise: wether or not to automatically deserialise spectral data
            timezone: the timezone that all the data will be converted to
        
        returns:
            dataframe with the requested values. deployment metadata values are just at the start of the dataframe,
            with null values for the rest of the column
        
        if the start and end times dont include the dataset, it will return an empty dataframe,
        if the start or end times are invalid, it will ignore it and include the whole dataset, subject to other conditions
        """
        if not os.path.isfile(self.db_name):
            raise Exception(f"database '{self.db_name}' does not exist")
        column_headers = self.load_table_names()
        all_column_headers = self.load_table_names()
        if "raw_data" in column_headers.keys():
            del column_headers["raw_data"]
        
        
        ##### if table is specified, check all columns exist
        if table is not None:
            for column in columns:
                if not column in column_headers[table] and raise_on_missing:
                    raise KeyError("column: '" +column+ "' was not found in table "+table)
        
        ##### remove duplicates
        non_dupe_columns = []
        for col in columns:
            if col not in non_dupe_columns:
                non_dupe_columns.append(col)
        columns = non_dupe_columns
        
        
        ##### make a list of all the column headers except accessory and a list of all the accessory column headers
        if table == "accessory_data":
            table_type = "accessory"
        else:
            column_headers, table_type = self.__guess_type(column_headers, columns)
        
        ##### find all table names and all column names for each table
        ##### nested for loops, but it will never have high iterations, executes in 1x10^-5s
        table_and_column_names = []
        output_columns = []
        for column in columns:
            found = False
            if table_type == "accessory":
                table_and_column_names.append(column)
                output_columns.append(column)
                found = True
            else:
                for key in column_headers:
                    if column in column_headers[key] and key != "raw":
                        found = True
                        table_and_column_names.append(key+"."+column)
                        output_columns.append(column)
                        break
            if not found and raise_on_missing:
                raise KeyError("column: '" +column+ "' was not found, maybe use 'load_metadata()' or 'load_accessory_data()")
        
        

        if columns == []:
            table_and_column_names = ["*"]
            if table is None:
                output_columns = all_column_headers["spectral_data"]+all_column_headers["system_data"]+all_column_headers["precalculated_values"]
            else:
                output_columns = all_column_headers[table]
        
        
        time_col = ""
        if table is not None:
            time_col = table+".pc_time_end_measurement"
        elif table_type == "normal":
            time_col = "spectral_data.pc_time_end_measurement"
        elif table_type == "accessory":
            time_col = "accessory_data.pc_time_end_measurement"
        
        
        
        time_condition = " WHERE "
        if start_time != None:
            if table_type == "deployment":
                raise Exception("selecting by time is invalid for deployment_metadata")
            times_after = time_col+" > \""+str(start_time)+"\" and "
            time_condition += times_after
        
        if end_time != None:
            if table_type == "deployment":
                raise Exception("selecting by time is invalid for deployment_metadata")
            times_before =  time_col+" < \""+str(end_time)+"\" and "
            time_condition += times_before
        
        if len(condition)>0:
            condition = time_condition + condition
        ##### check if there is a time condition(7 characters is " WHERE ")
        elif len(time_condition)>7:
            condition = time_condition[:-4]
        
        result = pd.DataFrame()
        if table is None:
            ##### fetch data from spectral data table and system data
            if len(table_and_column_names)>0 or columns == []:
                
                tables = list(column_headers.keys())
                
                main_table = tables[0]
                table_string = main_table
                for table_name in tables[1:]:
                    table_string += " LEFT JOIN " + table_name + " ON " + main_table+".sample_id = " + table_name + ".sample_id"
                sql = ""
                
                order_by = ""
                if "pc_time_end_measurement" in columns:
                    order_by = " ORDER BY STRFTIME('%s', "+time_col+")"
                
                if table_type == "accessory":
                    sql = "SELECT "+", ".join(table_and_column_names)+" FROM accessory_data"+condition
                    if sort:
                        sql += order_by
                elif table_type == "deployment":
                    sql = "SELECT "+", ".join(table_and_column_names)+" FROM deployment_metadata"+condition
                else:
                    sql = "SELECT "+", ".join(table_and_column_names)+" FROM " + table_string +condition
                    if sort:
                        sql += order_by
                
                result = self.load_sql(sql)
                
                if result is None:
                    raise ValueError("no data was returned by the query: "+sql)
                
                if not result.empty:
                    result.columns = output_columns
        
        else:
            ##### table has been specified
            column_list = ", ".join(columns)
            if columns == []:
                column_list = "*"
            sql = "SELECT " + column_list + " FROM "+table+condition
            result = self.load_sql(sql)
            if result is None:
                raise ValueError("no data was returned by the query: "+sql)
            
            if not result.empty:
                result.columns = output_columns
        
        ##### remove duplicated columns
        result = result.loc[:, ~result.columns.duplicated()].copy()
        
        if deserialise:
            ser = Serialisation("numpy")
            if "global_spectrum" in output_columns:
                result = ser.decode_dataframe(result, ["global_spectrum"])
            if "diffuse_spectrum" in output_columns:
                result = ser.decode_dataframe(result, ["diffuse_spectrum"])
        
        
        if "pc_time_end_measurement" in result.columns:
            timezone, timedelta = reformat().calculate_timezone(timezone)
            result["pc_time_end_measurement"] = pd.to_datetime(result["pc_time_end_measurement"], utc=True)
            result["pc_time_end_measurement"] = result["pc_time_end_measurement"].dt.tz_convert(timezone)#.dt.tz_localize(None)
        
        if len(result) == 0:
            raise ValueError("No data matches your query, check your start_time, end_time and any conditions")
        
        return result
    
    
    def load_raw(self, columns:[str]=[], 
                 start_time=None, 
                 end_time=None):
        """loads the raw data from the raw_data table
        
        params: 
            columns: list of columns that you want to load, they are in the format:
                "channel_0", "channel_1" etc.
                if [], all columns are loaded
            start_time, end_time: for only selecting data within a time period
                format: ISO-8601("2023-05-23 00:00:00")
                if you dont put in a full datetime, it will assume first timestamp,
                    e.g: 2023-05-23 will be read as 2023-05-23 00:00:00.
                    therefore, start_time is inclusive, end time is not
        returns:
            a dataframe with the requested data. pc_time_end_measurement is automatically added as a column
            columns = pc_time_end_measurement, requested_channel_0, requested_channel_1
            if only one column is requested, it is returned as one unpacked dataframe, index=time, columns=wavelength
        """
        parameter_columns = columns
        if columns == []:
            columns = self.load_table_names()
            
            if not "raw_data" in columns:
                raise ValueError("this database dosent have raw_data")
            
            columns = columns["raw_data"]
        
        
        if not os.path.isfile(self.db_name):
            raise ValueError(f"database '{self.db_name}' does not exist")
        
        if "pc_time_end_measurement" not in columns:
            columns = ["pc_time_end_measurement"]+columns
        
        time_col = "pc_time_end_measurement"
        
        time_condition = " WHERE "
        if start_time != None:
            times_after = time_col+" > \""+str(start_time)+"\" and "
            time_condition += times_after
        
        if end_time != None:
            times_before =  time_col+" < \""+str(end_time)+"\" and "
            time_condition += times_before
        
        if time_condition == " WHERE ":
            time_condition = ""

        ##### check if there is a time condition(7 characters is " WHERE ")
        elif len(time_condition)>7:
            time_condition = time_condition[:-4]

        sql = "SELECT "+", ".join(columns)+" FROM raw_data" + time_condition
        
        load = SqliteDBLoad(self.db_name)
        result = load.load_sql(sql)
        
        result.columns = columns
        
        ser = Serialisation("numpy")
        result = ser.decode_dataframe(result, columns[1:])
        
        if len(parameter_columns) == 1:
            result = pd.DataFrame(np.stack(result[parameter_columns[0]]), 
                                  index=result["pc_time_end_measurement"], 
                                  columns=np.arange(300, 1101))
        
        return result
    
    
    def load_metadata(self, columns:[str]=[], 
                      condition:str="", 
                      raise_on_missing:bool=True
                      ) -> pd.DataFrame:
        """loads metadata from the database
        params:
            columns: list of column names to extract from database, if empty, returns all
            condition: sql that comes after the WHERE
                e.g: gobal_molar>50
        returns:
            dataframe with the requested values.
        """
        return self.load(columns, condition=condition, 
                         table="deployment_metadata", raise_on_missing=raise_on_missing)
    
    def load_accessory(self, columns:[str]=[], 
                       start_time:str=None, 
                       end_time:str=None,
                       condition:str="",
                       raise_on_missing:bool=True,
                       sort:bool=True,
                       timezone:str="+00:00"
                       ) -> pd.DataFrame:
        """runs load with table="accessory". more readable than using the parameter, 
        as accessory cant be mixed with non accessory
        """
        table_names = self.load_table_names()
        
        if "accessory_data" not in table_names.keys():
            raise ValueError("this database dosent have accessory data")
        
        if columns == []:
            columns = table_names["accessory_data"]
        
        return self.load(columns, "accessory_data", start_time, end_time, condition,
                         raise_on_missing, sort, True, timezone)
    
    
    def load_spectrum(self, column,
                      table:str=None, 
                      start_time:str=None, 
                      end_time:str=None,
                      condition:str="",
                      raise_on_missing:bool=True,
                      sort:bool=True,
                      timezone:str="+00:00"
                      ) -> pd.DataFrame:
        """loads a single spectrum from the database and returns it as a dataframe
        
        params:
            column: which column to load
            table: which table to load data from. Not necessary but can be useful to specify when multiple tables have the same column
            start_time, end_time: for only selecting data within a time period
                format: ISO-8601("2023-05-23 00:00:00")
                if you dont put in a full datetime, it will assume first timestamp,
                    e.g: 2023-05-23 will be read as 2023-05-23 00:00:00.
                    therefore, start_time is inclusive, end time is not
            condition: sql that comes after the WHERE in an sql statement.
                e.g: gobal_integral>50
                if you want even more control, use load_sql
            raise_on_missing: how to handle when columns arent found, raise or just load if possible
            sort: sorts the results from the database
            deserialise: wether or not to automatically deserialise spectral data
            timezone: the timezone that all the data will be converted to
        
        returns:
            one dataframe containing the spectral data in the requested column
                columns = wavelengths values; 300-1100
                index = time of measurement
        """
        if not isinstance(column, str):
            raise TypeError("column must be a string. if you want to load multiple columns, call this function multiple times")
        
        data = self.load(["pc_time_end_measurement", column], table, start_time, end_time, condition,
                         raise_on_missing, sort, timezone)
        if len(data)>0:
            if isinstance(data.loc[0, column], np.ndarray):
                return pd.DataFrame(np.stack(data[column].values), index=data["pc_time_end_measurement"], columns=np.arange(300, 1101, 1))
            else:
                print("could not load spectrum, column was not a dataframe")
        else:
            print("could not load spectrum, no rows were returned from the dataframe")
        
        return pd.DataFrame()
    
        
    def load_sql(self, sql:str) -> pd.DataFrame:
        """loads data from a database using an sql query from the user
        
        params:
            sql: sql to select the desired data from the database
        
        returns:
            dataframe of the selected values
        """
        
        if not os.path.isfile(self.db_name):
            print("database: "+self.db_name+" does not exist")
            return None
        
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        data = cur.execute(sql).fetchall()
        con.close()
        
        if data == []:
            return None
        return pd.DataFrame(data)
    
    
    def __guess_type(self, column_headers, columns):
        """when the user dosent explicitly pass which table the requested columns are in,
        this code guesses what type of table the requested columns are in, 
        as you cant return data from different length tables at the same time.
        the types are:
            "normal": spectral_data, system_data, precalculated_values.
                readings every minute, on the minute.
            "accessory": accessory_data.
                readings every 10 seconds
            "deployment": deployment_metadata.
                one reading every dataseries
        """
        _type = "normal"
        if "accessory_data" in column_headers.keys() or "deployment_metadata" in column_headers.keys():
            normal_column_headers = column_headers.copy()
            
            accessory_column_headers = deployment_column_headers = []
            if "accessory_data" in column_headers.keys():
                accessory_column_headers = column_headers["accessory_data"]
                del normal_column_headers["accessory_data"]
            
            if "deployment_metadata" in column_headers.keys():
                deployment_column_headers = column_headers["deployment_metadata"]
                del normal_column_headers["deployment_metadata"]
            
            
            
            normal_column_headers_list = []
            for key in normal_column_headers:
                normal_column_headers_list += normal_column_headers[key]

            ##### one liner to remove duplicates from a list while preserving the order
            normal_column_headers_list = list(dict.fromkeys(normal_column_headers_list).keys())
            

            ##### remove time from the no_accessory list because it is also in accessory_data
            #####   this was causing errors when time and an accessory_data value were both selected, as 
            #####   only the spectral data time was being returned
            ##### this could cause issues if a user wants only the spectral data time, as theres no way to specify
            ##### currently defaults to spectral data if only pc_time is requested
            if "pc_time_end_measurement" in normal_column_headers_list and len(columns) > 1:
                normal_column_headers_list.remove("pc_time_end_measurement")
            
            check_columns = columns.copy()
            if "pc_time_end_measurement" in check_columns:
                check_columns.remove("pc_time_end_measurement")
            
            
            has_normal_data = np.isin(check_columns, normal_column_headers_list).any()
            has_deployment_data = np.isin(check_columns, deployment_column_headers).any()
            has_accessory_data = np.isin(check_columns, accessory_column_headers).any()
             
            ##### there are duplicate column names in different tables
            ##### where there are columns in multiple tables being selected, 
            #####   check if all the columns can be found in one table, then pick that table
            ##### if not, raise
            if has_accessory_data and has_normal_data:
                ##### is there a column being requested that is only in one table
                only_accessory = False
                only_normal = False
                for col in check_columns:
                    if col in normal_column_headers_list and col not in accessory_column_headers:
                        only_normal = True
                    if col in accessory_column_headers and col not in normal_column_headers_list:
                        only_accessory = True
                ##### if all requested columns in accessory are also in a normal table
                #####   ignore accessory and vice versa
                if only_normal and not only_accessory:
                    has_accessory_data = False
                if only_accessory and not only_normal:
                    has_normal_data = False
                if not only_normal and not only_accessory:
                    has_accessory_data = False
            
            
            
            ##### do same check for deployment
            if has_deployment_data and has_normal_data:
                ##### is there a column being requested that is only in one table
                only_deployment = False
                only_normal = False
                for col in check_columns:
                    if col in normal_column_headers_list and col not in deployment_column_headers:
                        only_normal = True
                    if col in deployment_column_headers and col not in normal_column_headers_list:
                        only_deployment = True
                
                ##### if all requested columns in deployment are also in a normal table
                #####   ignore deployment and vice versa
                if only_normal and not only_deployment:
                    has_deployment_data = False
                if only_deployment and not only_normal:
                    has_normal_data = False
                if not only_normal and not only_deployment:
                    has_deployment_data = False
            
            num_table_types = sum([has_normal_data, has_deployment_data, has_accessory_data])
            
            if num_table_types > 1 and len(columns) > 1:
                raise ValueError("You have requested data from incompatible tables (probably because they have unequal lengths). " + 
                                 "Make multiple seperate requests")
            
            if num_table_types == 1:
                if has_normal_data:
                    _type = "normal"
                if has_accessory_data:
                    _type = "accessory"
                if has_deployment_data:
                    _type = "deployment"
            
            
            if _type == "accessory":
                column_headers = {"accessory_data": column_headers["accessory_data"]}
            else:
                if "accessory_data" in column_headers.keys():
                    del column_headers["accessory_data"]
            
            if _type == "deployment":
                column_headers = {"deployment_metadata": column_headers["deployment_metadata"]}
            else:
                if "deployment_metadata" in column_headers.keys():
                    del column_headers["deployment_metadata"]
        
        return column_headers, _type