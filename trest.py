from main import *
from myparser import Parser

parser = Parser()
parser.setFile(OPENAPIFILE)

class TREST_Framework():


    def get_server(self):
        return SERVER
    def get_port(self):
        return PORT
    def get_hostname(self):
        return get_hostname_from_url()
    def get_protocol(self):
        return get_protocol()
    def get_all_paths(self):
        return parser.get_all_paths()
    def get_all_pathdata(self):
        return parser.get_all_pathdata()
    def get_all_path_info(self):
        return parser.get_all_path_data_params()
    def get_random_integer(self, start, end):
        value=random.randint(start,end)
        return value
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


