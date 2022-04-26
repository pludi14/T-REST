import requests

class VulnScanException(Exception):
    pass

from trest import TREST_Framework
trest=TREST_Framework()

def check_Server_Version():
    r=requests.head(url=trest.get_server())
    serverversion=r.headers["Server"]
    print(serverversion)

def run():
    check_Server_Version()
    return ["report"]