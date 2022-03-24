"""
T-REST: REST API Testing Tool by @MarcelPludra
"""

import sys
import time

from myparser import Parser
from tests.tests import Testgenerator
import requests
import logging
import http

from tlscheck import TLScheck

#OpenAPI description File
OPENAPIFILE = "/Users/mpludra/Library/CloudStorage/OneDrive-Personal/05_Wrexham/05_Project_COM646/Final_Project/carparkapi/openapi.json"

#Server Base URL
SERVER="172.16.114.134"

#Server Port
PORT="443"

#Debug Enabled
debug=True

# Turn on global debugging for the HTTPConnection class, doing so will
# cause debug messages to be printed to STDOUT
http.client.HTTPConnection.debuglevel = 0


version="Version: 0.1"
systemtime=str(time.asctime(time.localtime()))
programinfo="T-REST - "+ version +" - "+ systemtime +"\n" \
            "T-REST is a security testing tool for REST APIs. \n" \
            "This tool is designed only for security testing purposes! \n"

params = sys.argv[1:]  # Get Parameters

if len(params) == 0: # Check Paramaters: If zero then show Infor Message
    print(programinfo)
    print("Usage: python main.py [OPTIONS]")
    parmeterhelp="-d \t OpenAPI Sepcification File \n" \
                 "-s \t Service Base URL Example: 'https://server.com/api/v1/' \n" \
                 "-p \t Port of the target Service \n" \
                 "-d \t Enable debugging to file 'debug.log'"
    print(parmeterhelp)


# Parse Parameters -> https://www.tutorialspoint.com/argument-parsing-in-python
while params:

    if params[0] == "-d": # OpenAPI Specification File
        params.pop(0)
        OPENAPIFILE = params.pop(0)
        continue

    if params[0] == "-s": # Server Adress (URL)
        params.pop(0)
        SERVER= params.pop(0)
        continue

    if params[0] == "-p":  # Server Port
        params.pop(0)
        PORT = params.pop(0)
        continue

    if params[0] == "-d":  # Enable Debugging
        params.pop(0)
        debug=True
        continue
    break

#Start Debug to File "debug.log" if set in parameters
if debug:
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    logging.info('Debug started')


if __name__ == '__main__':

    p=Parser(OPENAPIFILE)
    t=Testgenerator(SERVER, PORT)
    tlstester=TLScheck(SERVER, PORT)
    #print(tlstester.check_medium_ciphers())
    print(tlstester.check_certificate())
    exit(0)






