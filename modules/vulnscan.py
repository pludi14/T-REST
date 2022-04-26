"""
T-REST - vulnscan.py: Vulnerability scan module by @MarcelPludra
"""

import requests

class VulnScanException(Exception):
    pass

from trest import TREST_Framework
trest=TREST_Framework()

def check_Server_Version():
    r=requests.head(url=trest.get_server())

    url = "api.cvesearch.com/search?q=CVE-2019-0708"

    print(response.text.encode('utf8'))


def run():
    check_Server_Version()
    return ["report"]