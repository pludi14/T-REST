"""
T-REST: REST API Testing Tool by @MarcelPludra
"""

import sys

from myparser import Parser
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
OPENAPIFILE = "/Users/mpludra/OneDrive/02_Arbeit/Python-Kurs/eigenerOrdner/specification.json"

SERVER="http://petstore.swagger.io/api/v2/"

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
    #print(p.get_all_paths())
    if p.get_servers() is not False:
        SERVER=p.get_servers()
        print(SERVER)

    url=SERVER[0]+"/api/projects"
    r = requests.get(url)
    print(r.status_code)
    print(r.json())





