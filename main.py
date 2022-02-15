"""
T-REST: REST API Testing Tool by @MarcelPludra
"""

import sys

from myparser import Parser

params = sys.argv[1:]  # Parameter in params aufnehmen
#OpenAPI description File
OPENAPIFILE = "/Users/mpludra/OneDrive/02_Arbeit/Python-Kurs/eigenerOrdner/python/openapi.json"

while params:
    if params[0] == "-d":
        params.pop(0)
        openapifile = params.pop(0)
        print()
        continue

    # if params[0] == "-s":
    #     params.pop(0)
    #     sleep = int(params.pop(0))
    #     continue

    break



if __name__ == '__main__':

    p=Parser(OPENAPIFILE)
    print(p.get_all_paths())
