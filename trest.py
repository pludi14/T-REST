"""
T-REST: T-REST Framework class by @MarcelPludra
"""

from main import *
from classes.myparser import Parser
import random
import urllib.parse


parser = Parser()
parser.setFile(get_Config()["openAPI"])

class TREST_Framework():

    #Get config from CONFIGFILE
    def get_Config(self):
        with open(CONFIGFILE, "r") as f:
            data = json.load(f)
        return data
    #Returns the server parameter value
    def get_server(self):
        return self.get_Config()["server"]

    #Returns the port parameter value
    def get_port(self):
        return self.get_Config()["port"]

    #Returns the hostname from specified URL
    def get_hostname(self):
        parsed_url = urllib.parse.urlparse(self.get_Config()["server"])
        return parsed_url.netloc

    # Returns the http protocol. http or https
    def get_protocol(self):
        parsed_url = urllib.parse.urlparse(self.get_Config()["server"])
        return parsed_url.scheme

    # Returns all paths as a list object
    def get_all_paths(self):
        return parser.get_all_paths()

    # Returns all paths and respective data as a dict object
    def get_all_pathdata(self):
        return parser.get_all_pathdata()

    # Returns all data from every path available as a dict object
    def get_all_path_info(self):
        return parser.get_all_path_data_params()

    # Returns all path data from a specific path as a dict object
    def get_path_data(self, path):
        return parser.get_pathdata(path)

    # Returns all paths with respective methods
    def get_path_methods(self):
        return parser.get_path_methods()

    # Returns a random integer value between 'start' and 'end'
    def get_random_integer(self, start, end):
        value=random.randint(start,end)
        return value

    # Returns a random string value with a specific 'length'
    def get_random_string(self, lenght):
        random_string = ""
        for _ in range(lenght+1):
            # Considering only upper and lowercase letters
            random_integer = random.randint(97, 97 + 26 - 1)
            flip_bit = random.randint(0, 1)
            # Convert to lowercase if the flip bit is on
            random_integer = random_integer - 32 if flip_bit == 1 else random_integer
            # Keep appending random characters using chr(x)
            random_string += (chr(random_integer))
        return random_string


