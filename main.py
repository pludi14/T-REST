"""
T-REST: REST API Testing Framework by @MarcelPludra
"""
import os
import time
from importlib.machinery import SourceFileLoader
from report import Report
from myparser import Parser
import http.client
import sys
import urllib.parse
import random


#OpenAPI description File
OPENAPIFILE = "/Users/mpludra/Library/CloudStorage/OneDrive-Personal/05_Wrexham/05_Project_COM646/Final_Project/carparkapi/openapi.json"

#Server Base URL
SERVER=""

#Server Port
PORT="443"

#Debug Enabled
debug=False

#Modules
modules={}
modulepath = os.getcwd()
modulepath=modulepath+"/modules/"

#Report
reportfile="Report.txt"
report=Report(reportfile)
write_report=False

program_run=True

# Turn on global debugging for the HTTPConnection class, doing so will
# cause debug messages to be printed to STDOUT
http.client.HTTPConnection.debuglevel = 0


version="Version: 1.0"
systemtime=str(time.asctime(time.localtime()))
programinfo="T-REST - "+ version +" - "+ systemtime +"\n" \
            "T-REST is a security testing framework for REST APIs. \n" \
            "This tool is designed only for security testing purposes! \n"

params = sys.argv[1:]  # Get Parameters

def check_params():
    if len(params) == 0: # Check Paramaters: If zero then show Info Message

        print("Usage: python main.py [OPTIONS]")
        parmeterhelp="-d \t OpenAPI Sepcification File \n" \
                     "-s \t Service Base URL Example: 'https://server.com/api/v1/' \n" \
                     "-p \t Port of the target Service \n"
        print(parmeterhelp)
        print("No parameters found. \n")





# Parse Parameters -> https://www.tutorialspoint.com/argument-parsing-in-python
while params:

    if params[0] == "-o": # OpenAPI Specification File
        params.pop(0)
        OPENAPIFILE = params.pop(0)
        # Create Parser Object with Parser File
        p = Parser(OPENAPIFILE)
        continue

    if params[0] == "-s": # Server Address (URL)
        params.pop(0)
        SERVER= params.pop(0)
        continue

    if params[0] == "-p":  # Server Port
        params.pop(0)
        PORT = params.pop(0)
        continue

    break





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
        return p.get_all_paths()
    def get_all_pathdata(self):
        return p.get_all_pathdata()
    def get_all_path_info(self):
        return p.get_all_path_data_params()
    def get_random_integer(self, start, end):
        value=random.randint(start,end)
        return value

    def get_random_string(self, lenght):
        random_string = ""
        for _ in range(100):
            # Considering only upper and lowercase letters
            random_integer = random.randint(97, 97 + 26 - 1)
            flip_bit = random.randint(0, 1)
            # Convert to lowercase if the flip bit is on
            random_integer = random_integer - 32 if flip_bit == 1 else random_integer
            # Keep appending random characters using chr(x)
            random_string += (chr(random_integer))
        return random_string

def get_hostname_from_url():
    parsed_url=urllib.parse.urlparse(SERVER)
    return parsed_url.netloc

def get_protocol():
    parsed_url = urllib.parse.urlparse(SERVER)
    return parsed_url.scheme

def check_modules():
    global modules
    files=os.listdir(modulepath)
    files.remove("__pycache__")
    if len(files)==0:
        print("No modules found in folder (./modules)")
    cnt = 0
    for file in files:
        modules[cnt]=file
        cnt=cnt+1

def check_connection():
    pass


def run_modules(selected):
    global modules
    mod={}
    try:
        for number in selected:
            number=int(number)
            modpath=modulepath+modules[number]
            modname=modules[number].strip(".py")
            mod = SourceFileLoader(modname, modpath).load_module()
            modulerunner(mod,modname)

    except Exception as e:
        print("Failure in run_module:" + e)


def modulerunner(mod,modname):
    try:
        result=mod.run()
        if write_report:
            report.add_module_report(result, modname)
            print("Module "+ modname + " finished!")
    except Exception as e:
        print("Failure in modulerunner "+modname+": " + str(e))
        if write_report:
            report.add_module_exception_report(e,modname)


def module_selection():
    print("Modules found in folder " + modulepath +":")
    for number,module in modules.items():
        print(str(number) + ":\t" + module)
    print("a:\tRun all modules")
    print("b:\tGo back")
    selected=input("Please select the modules you want to run: ")
    if selected=="b":
        return "b"
    if selected=="a":
        selected=list(modules.keys())
    else:
        selected = selected.split(",")

    return selected

def parser_menu():
    print("This is the parser menu. Not finished yet!")


menu="\n" \
     "Options: \n" \
     "m: \t Run modules \n" \
     "p: \t Show parser menu \n" \
     "h: \t Show this menu again \n" \
     "q: \t Quit program"



if __name__ == '__main__':
    print(programinfo)

    check_params()
    check_modules()

    print(menu)
    sel_option=input()
    while program_run:
        if sel_option=="m":
            selected=module_selection()
            if len(selected)!=0:
                if selected == "b":
                    pass
                else:
                    run_modules(selected)
            else:
                print("No modules selected")
        if sel_option=="p":
            parser_menu()
        if sel_option=="h":
            print(menu)
        if sel_option=="q":
            exit(0)
        else:
            "No valid option!"


        sel_option=""
        print(menu)
        sel_option = input()









