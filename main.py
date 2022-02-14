# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import sys

from parser import Parser

params = sys.argv[1:]  # Parameter in params aufnehmen
#OpenAPI description File
openapifile = "/Users/mpludra/OneDrive/02_Arbeit/Python-Kurs/eigenerOrdner/python/openapi.json"

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

def parseDescription(description):
    p=Parser(description)
    print(p)



if __name__ == '__main__':

    parseDescription(openapifile)
