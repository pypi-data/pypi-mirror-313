# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""
import os

import hsr1

db_loc = "databases/synthetic/"

output_location = "C:/Users/albie/Dropbox/Albie (1)/synthetic dataset images"

winster = {"lat":53.14,
           "lon":-1.63,
           "alt":227.0}

n_pole = {"lat":90,
          "lon":0,
          "alt":0}

svalbard = {"lat":77,
            "lon":50,
            "alt":0}


def create_001(plot=True, **kwargs):
    """Standard: 
    spectral_data period: 1min
    system_data period: 1min
    accessory_data period: 10s
    integral source: pvlib
    location: Winster
    duration: 1 month"""
    
    db_name = db_loc+"001.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2024-02-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1min")
    dataset.generate_accessory_data("10s")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_001()
    
def plot_001(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "001"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_0011(plot=True, **kwargs):
    """Standard: 
    spectral_data period: 1min
    system_data period: 1min
    accessory_data period: 10s
    integral source: pvlib
    location: Winster
    duration: 1 month"""
    
    db_name = db_loc+"0011.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2023-11-01 00:00:00+00:00",
                                                     end_date="2024-03-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("10min")
    dataset.generate_accessory_data("10min")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_0011()
    
def plot_0011(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "0011"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)
    


def create_002(plot=True, **kwargs):
    """spectral_data period: 1min
    system_data period: 10min
    accessory_data period: 10s
    integral source: pvlib
    location: Winster
    Duration: 1 month"""
    
    db_name = db_loc+"002.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2024-02-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1min")
    dataset.generate_system_data("10min")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_002()

def plot_002(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "002"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_003(plot=True, **kwargs):
    """spectral_data period: 10min
    system_data period: 1h
    accessory_data period: 10min
    integral source: pvlib
    location: Winster
    Duration: 1 month"""
    
    db_name = db_loc+"003.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2024-02-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("10min")
    dataset.generate_system_data("1h")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_003()

def plot_003(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "003"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_004(plot=True, **kwargs):
    """spectral_data period: 1h
    system_data period: 1h
    accessory_data period: 1h
    integral source: pvlib
    location: Winster
    Duration: 1 month"""
    
    db_name = db_loc+"004.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2024-02-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1h")
    dataset.generate_system_data("1h")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_004()

def plot_004(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "004"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_005(plot=True, **kwargs):
    """spectral_data period: 1h
    system_data period: 1h
    accessory_data period: 1h
    integral source: pvlib
    location: Winster
    Duration: 1 month"""
    
    db_name = db_loc+"005.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2025-01-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1h")
    dataset.generate_system_data("1h")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_005()

def plot_005(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "005"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_006(plot=True, **kwargs):
    """spectral_data period: 10s
    system_data period: 1min
    accessory_data period: 10s
    Integral source: pvlib
    Location: Winster
    Duration: 1 Week
    """
    
    db_name = db_loc+"006.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2024-01-08 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("10s")
    dataset.generate_system_data("1min")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_006()

def plot_006(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "006"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_007(plot=True, **kwargs):
    """spectral_data period: 10s
    system_data period: 1min
    accessory_data period: 10s
    Integral source: pvlib
    Location: Winster
    Duration: 1 Week
    Notes: data is not taken on the minute, instead 5s past the minute
    """
    
    db_name = db_loc+"007.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:05+00:00",
                                                     end_date="2024-01-08 23:59:05+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("10s")
    dataset.generate_system_data("1min")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_007()

def plot_007(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "007"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_008(plot=True, **kwargs):
    """spectral_data period: 1min
    system_data period: 1min
    accessory_data period: 10s
    Integral source: pvlib
    Location: Winster
    Duration: 1 day
    """
    
    db_name = db_loc+"008.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:05+00:00",
                                                     end_date="2024-01-01 23:59:05+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1min")
    dataset.generate_system_data("1min")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_008()

def plot_008(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "008"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_009(plot=True, **kwargs):
    """spectral_data period: 1min
    system_data period: 1min
    accessory_data period: 10s
    Integral source: pvlib
    Location: Winster
    Duration: 1 day
    note: missing data at 12 midday
    """
    
    db_name = db_loc+"009.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:05+00:00",
                                                     end_date="2024-01-01 23:59:05+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1min")
    dataset.generate_system_data("1min")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    for i in range(12):
        dataset.remove_rows("spectral_data", dataset.remove_n_hour, i)
    dataset.remove_rows("spectral_data", dataset.remove_n_hour, 23)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_009()

def plot_009(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "009"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_010(plot=True, **kwargs):
    """spectral_data period: 1min
    system_data period: 1min
    accessory_data period: 10s
    Integral source: pvlib
    Location: north pole
    Duration: 1 Week
    """
    
    db_name = db_loc+"010.db"
    
    location = n_pole
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-06-01 00:00:00+00:00",
                                                     end_date="2024-06-08 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1min")
    dataset.generate_system_data("1min")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_010()

def plot_010(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "010"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_011(plot=True, **kwargs):
    """spectral_data period: 1h
    system_data period: 1h
    accessory_data period: 1h
    Integral source: pvlib
    Location: north pole
    Duration: 1 Year
    """
    
    db_name = db_loc+"011.db"
    
    location = n_pole
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2025-01-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1h")
    dataset.generate_system_data("1h")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_011()

def plot_011(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "011"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_012(plot=True, **kwargs):
    """spectral_data period: 1min
    system_data period: 1min
    accessory_data period: 1min
    Integral source: pvlib
    Location: north pole
    Duration: 2 months(over the sunrise day)
    """
    
    db_name = db_loc+"012.db"
    
    location = n_pole
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-03-01 00:00:00+00:00",
                                                     end_date="2024-05-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1h")
    dataset.generate_system_data("1h")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_012()

def plot_012(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "012"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_013(plot=True, **kwargs):
    """spectral_data period: 1h
    system_data period: 1h
    accessory_data period: 1h
    Integral source: pvlib
    Location: svalbard
    Duration: 1 Year
    """
    
    db_name = db_loc+"013.db"
    
    location = svalbard
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2025-01-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1h")
    dataset.generate_system_data("1h")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_013()

def plot_013(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "013"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_014(plot=True, **kwargs):
    """spectral_data period: 1h
    system_data period: 1h
    accessory_data period: 1h
    Integral source: pvlib
    Location: svalbard
    Duration: 4 Months
    """
    
    db_name = db_loc+"014.db"
    
    location = svalbard
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2024-05-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1h")
    dataset.generate_system_data("1h")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_014()

def plot_014(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "014"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_100(plot=True, **kwargs):
    """spectral_data period: 1min
    system_data period: 1min
    accessory_data period: 1min
    Integral source: hour of day
    Location: winster
    Duration: 1 Month
    """
    
    db_name = db_loc+"100.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2024-02-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1min")
    dataset.generate_system_data("1min")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.integral_hour_of_day)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_100(**kwargs)

def plot_100(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "100"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_101(plot=True, **kwargs):
    """spectral_data period: 1h
    system_data period: 1h
    accessory_data period: 1h
    Integral source: hour of day
    Location: winster
    Duration: 1 Month
    """
    
    db_name = db_loc+"101.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2024-02-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1h")
    dataset.generate_system_data("1h")
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.integral_hour_of_day)
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_101(**kwargs)

def plot_101(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "101"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_102(plot=True, **kwargs):
    """spectral_data period: 1m
    system_data period: 1h
    accessory_data period: 10s
    Integral source: pvlib
    Location: winster
    Duration: 1 Month
    system data calculated from accesory_data
    data is mobile, no default latitude/longitude, should have gaps in elv/azi plot
        where precalculated_values couldnt be calculated
    """
    
    db_name = db_loc+"102.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 00:00:00+00:00",
                                                     end_date="2024-02-01 23:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1min")
    dataset.generate_accessory_data("10s")
    dataset.remove_rows("accessory_data", dataset.remove_n_hour, 12)
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    def return_speech_marks():
        return ["''"]*3
    
    dataset.generate_custom_column("deployment_metadata", ["default_elevation", "default_latitude", "default_longitude"], return_speech_marks)
    
    
    dfs = dataset.get_dfs()
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_102(**kwargs)

def plot_102(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "102"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


def create_103(plot=True, **kwargs):
    """spectral_data period: 1m
    accessory_data period: 10s
    Integral source: pvlib
    Location: winster
    Duration: 1 Day
    system data calculated from accesory_data
    missing data from 12-3pm
    """
    
    db_name = db_loc+"103.db"
    
    location = winster
    
    if os.path.exists(db_name):
        print("overwriting database")
        os.remove(db_name)

    dataset = hsr1.synthetic_dataset.SyntheticDataset(start_date="2024-01-01 09:00:00+00:00",
                                                     end_date="2024-01-01 19:59:00+00:00",
                                                     latitude=location["lat"],
                                                     longitude=location["lon"],
                                                     altitude=location["alt"])
    dataset.generate_spectral_data("1min")
    dataset.remove_rows("spectral_data", dataset.remove_n_hour, 12)
    dataset.remove_rows("spectral_data", dataset.remove_n_hour, 13)
    dataset.remove_rows("spectral_data", dataset.remove_n_hour, 14)
    
    dataset.generate_accessory_data("10s")
    
    dataset.generate_custom_column("accessory_data", "Latitude", dataset.num_readings, base=location["lat"], scale=0.001)
    dataset.generate_custom_column("accessory_data", "Longitude", dataset.num_readings, base=location["lon"], scale=0.001)
    
    dataset.generate_system_data_accessory()
    dataset.generate_deployment_metadata("C:/Users/albie/work/Datasets/Winster 2023/HSR1-002 Winster 2024 Deployment.ini")
    
    dataset.generate_custom_column("spectral_data", 
                                   ["global_integral", "diffuse_integral"], 
                                   dataset.pvlib_integral_static)
    
    # def return_speech_marks():
    #     return ["''"]*3
    
    # dataset.generate_custom_column("deployment_metadata", ["default_elevation", "default_latitude", "default_longitude"], return_speech_marks)
    
    
    dfs = dataset.get_dfs()
    dfs = (dfs[0], dfs[1], dfs[2])
    
    db = hsr1.DBDriver(db_name)
    db.store(dfs)
    
    if plot:
        plot_103(**kwargs)

def plot_103(integral=True, gps=False, dips=False, accessory=False, plot_all=False, **kwargs):
    db_num = "103"
    
    if plot_all:
        integral=True
        gps=True
        dips=True
        accessory=True
    
    db_name = db_loc+db_num+".db"
    graph = hsr1.Graph(db_name, output_location=output_location+"/"+db_num, **kwargs)
    
    if integral:
        graph.plot_integral(title="synthetic dataset "+db_num, **kwargs)
    if gps:
        graph.plot_gps(title="synthetic dataset "+db_num)
    if dips:
        graph.plot_dips_summary(title="synthetic dataset "+db_num)
    if accessory:
        graph.plot_accessory(title="synthetic dataset "+db_num)


