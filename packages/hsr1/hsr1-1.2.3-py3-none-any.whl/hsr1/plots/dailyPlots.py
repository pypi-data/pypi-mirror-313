# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import math

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import hsr1.plots.graphUtils as graphUtils
import hsr1.plots.flagData as flagData

class DailyPlots:
    def __init__(self, columns, data, title_prefix, output_location=None, flag=False, max_limit=None, min_limit=None, block=True):
        self.columns = columns
        self.title_prefix = title_prefix
        self.output_location = output_location
        self.flag = flag
        self.block = block
        
        data = data.copy()
        
        ##### if dni is one of the columns, set ylimit according to the next 100 from ghi
        ##### as dfi has big spikes near sunset
        min_max_columns = self.columns.copy()
        if "direct_normal_integral" in min_max_columns:
            min_max_columns.remove("direct_normal_integral")
            if not "global_integral" in min_max_columns:
                min_max_columns.append("global_integral")
                data["global_integral"] = ((((data["global_integral"]+10)/100)+1)*100).astype(int)
            
        self.max = np.nanmax(data[min_max_columns].replace({np.inf: np.nan}).values) if max_limit is None else max_limit
        self.min = np.nanmin(data[min_max_columns].replace({np.inf: np.nan}).values) if min_limit is None else min_limit
        
        self.flags = None
        self.flag_columns = None
        
        if flag:
            self.flags = flagData.flag(data, True)
            self.flag_columns = self.flags.columns
    
    
    def plot_row(self, axes, data, dates, day_format:str="%d", legend=False):
        df = data.copy()
        
        df["pc_time_end_measurement"] = pd.to_datetime(df["pc_time_end_measurement"])
        axes.set_xlim(min(df["pc_time_end_measurement"]), max(df["pc_time_end_measurement"]))
        for column in self.columns:
            label_column = column
            if label_column[0] == "_":
                label_column = label_column[1:]
            axes.plot(df["pc_time_end_measurement"], df[column], linewidth=0.5, label=label_column)
        
        if self.flag:
            df[self.flag_columns] = df[self.flag_columns].astype(float).fillna(0)
            any_flags = df[self.flag_columns].any(axis=1)
            df.loc[:, self.columns] = df.loc[:, self.columns].fillna(0)
            for column in self.columns:
                flag_df = pd.DataFrame()
                flag_df["pc_time_end_measurement"] = df["pc_time_end_measurement"]
                flag_df[column] =  df.loc[any_flags, column]
                axes.plot(flag_df["pc_time_end_measurement"], flag_df[column], color=(1,0,1), linewidth=0.5)
        
        axes.set_ylim(self.min, self.max)
        if legend:
            ##### accounting for different matplotlib versions
            mpl_version = matplotlib.__version__
            mpl_version = mpl_version.split(".")
            if int(mpl_version[0]) > 3 or (int(mpl_version[0]) == 3 and int(mpl_version[1]) > 5):
                legend = axes.legend(loc='upper center', ncols=len(self.columns))
                for leg in legend.legend_handles:
                    leg.set_linewidth(3)
            else:
                legend = axes.legend(loc='upper center', ncol=len(self.columns))
        
        labels = []
        for date in dates:
            labels.append(pd.Timestamp(date).strftime(day_format).lstrip("0")) if date != "" else labels.append("")
            labels.append("")
        labels.append("")
        
        xlims = axes.set_xlim()
        daynos = np.linspace(xlims[0], xlims[1], 2*(len(dates))+1)
        axes.set_xticks(daynos, labels)
    
    
    def plot_month(self, df, rows, days_in_row):
        df = df.copy()
        if rows == None and days_in_row == None:
            rows = 5
            days_in_row = 7
        
        if rows == None:
            x = 31//days_in_row
            rows = x if 31 % days_in_row == 0 else x + 1
            
        elif days_in_row == None:
            x = 31//rows
            days_in_row = x if 31 % rows == 0 else x + 1
        
        month = str(df["pc_time_end_measurement"].iloc[0].year) + "-" + str(df["pc_time_end_measurement"].iloc[0].month)
        month_timestamp = pd.Timestamp(month)
        
        month_int = df["pc_time_end_measurement"].iloc[0].year*10+df["pc_time_end_measurement"].iloc[0].month
        
        row_dates = []
        for i in range(rows):
            row_dates.append([])
            for j in range(i*days_in_row, (i+1)*days_in_row):
                # row_dates[i].append((month_timestamp + pd.Timedelta(j, "days")).strftime("%Y-%m-%d"))
                row_dates[i].append((month_timestamp + pd.Timedelta(j, "days")).date())
        timestamps_in_month = df["pc_time_end_measurement"].dt.year*10+df["pc_time_end_measurement"].dt.month == month_int
        last_day_of_month = df.loc[timestamps_in_month].iloc[len(df)-1]["pc_time_end_measurement"].date
        day_one = pd.Timestamp(df['pc_time_end_measurement'].iloc[0])
        title = f"{day_one.strftime('%B')} {day_one.strftime('%Y')}"
        self.plot_page(row_dates, df, last_day_of_month, title)
    
    def plot_int(self, df:pd.DataFrame, period:int, rows:int=None, days_in_row:int=None):
        df = df.copy()
        ##### if insufficient rows/days_in_row are given make a best guess from the period and any given values
        if rows == None and days_in_row == None:
            x = math.sqrt(period)
            rows = days_in_row = int(x) if x % 1 == 0 else int(x) + 1
            
        elif rows == None:
            x = period//days_in_row
            rows = x if period % days_in_row == 0 else x + 1
            
        elif days_in_row == None:
            x = period//rows
            days_in_row = x if period % rows == 0 else x + 1
        
        num_days_in_page = rows*days_in_row
        all_days = df["pc_time_end_measurement"].dt.date.unique()
        num_pages = len(all_days)//num_days_in_page if len(all_days) % num_days_in_page == 0 else len(all_days)//num_days_in_page + 1
        
        
        
        page_days = [all_days[i*num_days_in_page:(i+1)*num_days_in_page] for i in range(num_pages)]
        
        for days in page_days:
            
            first_day = days[0]
            row_dates = []
            for i in range(rows):
                this_row = []
                for j in range(days_in_row):
                    this_row.append(first_day + pd.Timedelta(i*days_in_row+j, "days"))
                row_dates.append(this_row)
            
            last_valid_day = all_days[-1]
            
            title = ""
            months = pd.Series(pd.to_datetime(days)).dt.strftime("%B").unique()
            if len(months) == 1:
                title += months[0]
            else:
                title += ", ".join(months[:-1]) + " and " + months[-1]
            
            title += " "            
            years = pd.Series(pd.to_datetime(days)).dt.year.unique()
            if len(years) == 1:
                title += str(years[0])
            else:
                title += ", ".join(str(years[:-2])) + " and " + str(years[-1])
            
            
            self.plot_page(row_dates, df, last_valid_day, title, "%b-%d")
            
    
    
    def plot_page(self, row_dates, data, last_valid_day, title, day_format:str="%d"):
        df = data.copy()
        
        ##### dosent include last day, stops at the start of it
        all_seconds = [pd.date_range(pd.Timestamp(row[0]), pd.Timestamp(row[-1]) + pd.Timedelta(1, "day"), freq="min") for row in row_dates]
        
        all_seconds_dfs = [pd.DataFrame(row, columns=["pc_time_end_measurement"]) for row in all_seconds]
        
        df["pc_time_end_measurement"] = df["pc_time_end_measurement"].dt.tz_localize(None)
                
        row_dfs = [df.loc[np.isin(df["pc_time_end_measurement"].dt.date, row)] for row in row_dates]
        row_dfs = [pd.merge(all_seconds_dfs[i], row_dfs[i], on="pc_time_end_measurement", how="outer") for i in range(len(all_seconds_dfs))]
        
        full_title = self.title_prefix+title
        fig, axes = plt.subplots(len(row_dates), figsize=(16.5, 11.7))
        if isinstance(axes, matplotlib.axes._axes.Axes):
            axes = [axes]
        
        fig.suptitle(full_title)
        plt.tight_layout()
        
        last_valid_day_count = 0
        for i, row in enumerate(row_dates):
            for j, date in enumerate(row):
                if last_valid_day_count >= 1:
                    row_dates[i][j] = ""
                if date == last_valid_day:
                    last_valid_day_count += 1
                
        legend = True
        for i, df in enumerate(row_dfs):
            self.plot_row(axes[i], df, row_dates[i], day_format=day_format, legend=legend)
            legend=False
        
        full_title = graphUtils.make_full_title(full_title)
        
        if self.output_location is not None:
            plt.savefig(self.output_location+"/daily_plots_"+full_title+".png")
        plt.show(block=self.block)
    
    
    def plot_series(self, period, rows, days_in_row, data, ignore_zeros=False):
        """
        params:
            period: how many days per page, "monthly", "weekly", integer
        """
        data = data.copy()
        # self.max_integral = (int((self.max_integral+10)/100)+1)*100
        if self.flag:
            data = pd.merge(data, self.flags, left_index=True, right_index=True)
        if ignore_zeros:
            data = data.replace({0:np.nan})
        
        pages_dfs = pd.DataFrame()
        
        if type(period) == type(0):
            self.plot_int(data, period, rows, days_in_row)
        
        elif period == "monthly":
            
            # years_and_months = np.unique(list(zip(data["pc_time_end_measurement"].dt.month.to_numpy(), 
            #                                       data["pc_time_end_measurement"].dt.year.to_numpy())), 
            #                              axis=0)
            years_and_months = data["pc_time_end_measurement"].dt.year*100+data["pc_time_end_measurement"].dt.month
            
            pages_dfs = [data.loc[data["pc_time_end_measurement"].dt.year*100+data["pc_time_end_measurement"].dt.month == year_and_month] for year_and_month in years_and_months.unique()]
        
            for df in pages_dfs:
                self.plot_month(df, rows, days_in_row)
        
        elif period == "weekly":
            if rows == None:
                rows = 5
            days_in_row = 7
            period = 7 * rows
            self.plot_int(data, period, rows, days_in_row)
        