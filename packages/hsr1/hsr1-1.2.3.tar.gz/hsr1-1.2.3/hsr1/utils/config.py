# -*- coding: utf-8 -*-
"""
copyright 2024 Peak Design
this file is part of hsr1, which is distributed under the GNU Lesser General Public License v3 (LGPL)
"""

from configparser import ConfigParser
import os

class Config:
    def __init__(self, filepath:str):
        self.filepath = filepath
    
    def read_section(self, section_name:str) -> dict:
        """reads a section of the initialised config file
        params:
            section_name: the name of the section to be read
        returns:
            config: a dictionary of all the fields in the relevant section
        """
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(f"config file \"{self.filepath}\" not found")
        
        parser = ConfigParser()
        parser.read(self.filepath)
        
        config = {}
        
            
        if parser.has_section(section_name):
            params = parser.items(section_name)
            
            for param in params:
                config[param[0]] = param[1]

        else:
            print("section not found in config file")
            return
        
        return config