"""
T-REST: REST API Testing Tool by @MarcelPludra
"""
import logging

import time
import urllib.parse

from myparser import Parser
from tests.tests import Testgenerator
import requests
from setup_logger import logger
import http
import sys
from tlscheck import TLScheck

#Setup Logging
logger=logging.getLogger("main")
logger.info('Debug started')

#OpenAPI description File
OPENAPIFILE = "/Users/mpludra/Library/CloudStorage/OneDrive-Personal/05_Wrexham/05_Project_COM646/Final_Project/carparkapi/openapi.json"

#Server Base URL
SERVER=""

#Server Port
PORT="443"

#Debug Enabled
debug=False

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
    exit(0)


# Parse Parameters -> https://www.tutorialspoint.com/argument-parsing-in-python
while params:

    if params[0] == "-o": # OpenAPI Specification File
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

    break




def get_hostname_from_url():
    parsed_url=urllib.parse.urlparse(SERVER)
    return parsed_url.netloc

def is_https():
    ishttps=False
    parsed_url = urllib.parse.urlparse(SERVER)
    if parsed_url.scheme=="https":
        ishttps=True
    return ishttps

def check_TLS(tlstester):
    #print(tlstester.check_medium_ciphers())
    print(tlstester.check_certificate())

if __name__ == '__main__':

    #p=Parser(OPENAPIFILE)
    t=Testgenerator(SERVER, PORT)

    if is_https():
        tlstester=TLScheck(get_hostname_from_url(), PORT)
        check_TLS(tlstester)
    else:
        logger.info("Application does not support https!")
        print("Application does not support https!")

    exit(0)






