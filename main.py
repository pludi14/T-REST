"""
T-REST: REST API Testing Tool by @MarcelPludra
"""

import sys

from myparser import Parser
from tests.tests import Testgenerator
import requests
import logging
import http

# Set up logging to a file
logging.basicConfig(filename="app.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Turn on global debugging for the HTTPConnection class, doing so will
# cause debug messages to be printed to STDOUT
http.client.HTTPConnection.debuglevel = 0




params = sys.argv[1:]  # Parameter in params aufnehmen
#OpenAPI description File
#OPENAPIFILE = "/Users/mpludra/Library/CloudStorage/OneDrive-Personal/05_Wrexham/05_Project_COM646/Final_Project/carparkapi/openapi.json"
OPENAPIFILE= "/Users/mpludra/Library/CloudStorage/OneDrive-Personal/02_Arbeit/Python-Kurs/specification.json"
SERVER="http://mp.api"
PORT="8080"

while params:
    if params[0] == "-d":
        params.pop(0)
        OPENAPIFILE = params.pop(0)
        print()
        continue

    if params[0] == "-s":
        params.pop(0)
        SERVER= params.pop(0)
        continue

    break


if __name__ == '__main__':

    p=Parser(OPENAPIFILE)
    path="/api/projects"
    data=p.get_pathdata(path)



    if p.get_servers() is not False:
        SERVER=p.get_servers()
        PORT=443


    t=Testgenerator(SERVER[0], PORT)
    t.check_request(data, path)

    #url=SERVER+"/v1/cars"
    #print(url)
    #r = requests.get(url)
    #print(r.status_code)
    #print(r.json())







