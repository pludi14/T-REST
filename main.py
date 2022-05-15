"""
T-REST: REST API Testing Framework by @MarcelPludra
"""
import importlib
import os
import time
from importlib.machinery import SourceFileLoader
from classes.report import Report
from classes.myparser import Parser
import http.client
import sys
import urllib.parse
import json

########
#OpenAPI description file and parser object variable declaration
OPENAPIFILE = ""
p=Parser()

#Server Base URL
SERVER=""

#Server Port
PORT=""

#Modules
modules={}
modulepath = os.getcwd()
modulepath=modulepath+"/modules/"

#Report
reportfile=os.getcwd()+"/Report"
report=Report(reportfile)
write_report=True

#Automation Mode
AUTO=False
AUTO_MODULES=""

# Turn on global debugging for the HTTPConnection class, doing so will
# cause debug messages to be printed to STDOUT
http.client.HTTPConnection.debuglevel = 0

# Program Version and Start Message
version="Version: 1.1"
systemtime=str(time.asctime(time.localtime()))
programinfo="T-REST - "+ version +" - "+ systemtime +"\n" \
            "T-REST is a security testing framework for REST APIs. \n" \
            "This tool is designed only for security testing purposes! \n"

params = sys.argv[1:]  # Get Parameters
if len(params) == 0: # Check Paramaters: If zero then show Info Message
    print("Usage: python main.py [OPTIONS]")
    parmeterhelp="-d \t OpenAPI Sepcification File \n" \
                 "-s \t Server Base URL Example: 'https://server.com/api/v1/' \n" \
                 "-p \t Port of the target Service \n" \
                 "-a \t Automation mode \n"
    print(parmeterhelp)
    print("No parameters found. \n")


# Parse Parameters
while params:
    if params[0] == "-d": # OpenAPI Specification File
        params.pop(0)
        OPENAPIFILE = params.pop(0)
        continue

    if params[0] == "-s": # Server Address (URL)
        params.pop(0)
        SERVER= params.pop(0)
        continue

    if params[0] == "-p":  # Server Port
        params.pop(0)
        PORT = params.pop(0)
        continue

    if params[0] =="-a":
        params.pop(0)
        AUTO=True
        AUTO_MODULES=params.pop(0)
        continue
    break

# Sets the OpenAPI file in the parser class
def set_parser_OpenAPI_file():
    global OPENAPIFILE, p
    p.setFile(OPENAPIFILE)


# Returns the hostname from specified UR
def get_hostname_from_url():
    parsed_url=urllib.parse.urlparse(SERVER)
    return parsed_url.netloc

# Returns the http protocol. http or https
def get_protocol():
    parsed_url = urllib.parse.urlparse(SERVER)
    return parsed_url.scheme

#Checks if modules are available in folder 'modules' and creates the 'modules' variable
def check_modules():
    global modules
    files=os.listdir(modulepath)
    if "__pycache__" in files:
        files.remove("__pycache__")
    if len(files)==0:
        print("No modules found in folder (./modules)")
    cnt = 0
    for file in files:
        modules[cnt]=file
        cnt=cnt+1

# Returns the number to a modulename
def get_number_to_modulename(modulenames):
    global modules
    numbers=[]
    for selected_name in modulenames:
        for nr, name in modules.items():
            modname=name.strip(".py")
            if modname == selected_name:
                numbers.append(nr)
    return numbers

# Executes a specific module
def modulerunner(mod,modname):
    try:
        result=mod.run()
        if write_report:
            report.add_module_report(result, modname)
            print("Module "+ modname + " finished!")
    except Exception as e:
        print("Failure in modulerunner "+modname+": " + str(e))
        del mod
        if write_report:
            report.add_module_exception_report(e,modname)

# Imports the selceted modules and executes it with the modulerunner() function
def run_modules(selected):
    global modules


    for number in selected:
        number=int(number)
        modpath=modulepath+modules[number]
        modname=modules[number].strip(".py")
        try:
            mod = SourceFileLoader(modname, modpath).load_module()
        except Exception as e:
            print("Failure in run_modules. Module cannot be loaded: " + str(e))
            return
        modulerunner(mod,modname)


# Function for control Module Submenu
def module_menu():
    print("Modules found in folder " + modulepath +":")
    for number,module in modules.items():
        print(str(number) + ":\t" + module)
    print("a:\tRun all modules")
    print("b:\tGo back")
    selected=input("Please select the modules you want to run: ")
    if selected=="b":
        return
    if selected=="a":
        selected=list(modules.keys())
    else:
        selected = selected.split(",")

    if len(selected) != 0:
        if selected == "b":
            return
        else:
            try:
                run_modules(selected)
            except Exception as e:
                print("Failure in module selection.: ")
                print(e)
    else:
        print("No modules selected")


# Main menu text generation and print to stdout
def print_main_menu():
    if write_report:
        reportstatus="Enabled"
    else:
        reportstatus = "Disabled"
    menutext= "\n" \
              "Main menu: \n" \
              "m: \t Run modules \n" \
              "p: \t Show OpenAPI parser menu \n" \
              "r: \t Show report menu. Report status: " + reportstatus + "\n" \
              "s: \t Show server menu \n"\
              "h: \t Show this menu again \n" \
              "q: \t Quit program"
    print(menutext)

# Parser menu text generation and print to stdout
def print_parser_menu():
    global OPENAPIFILE
    if write_report:
        reportstatus="Enabled"
    else:
        reportstatus = "Disabled"
    menutext = "\n" \
               "OpenAPI specification file: " + OPENAPIFILE + "\n" \
               "Parser Menu: \n" \
               "a: \t Show all paths \n" \
               "p: \t Show all paths + additional path information \n" \
               "P: \t Show all paths + path method and parameters \n" \
               "m: \t Show all paths + path methods \n" \
               "c: \t Change OpenAPI specification file path \n" \
               "h: \t Show this menu again \n" \
               "b: \t Go back"
    print(menutext)

# Function for control Parser Submenu
def parser_menu():
    global p, OPENAPIFILE
    if p is not None:
        print_parser_menu()
        state=True
        user_input = input()
        valid_input = False
        while state:
            if user_input=="a":
                valid_input = True
                print(p.get_all_paths())
            if user_input=="p":
                valid_input = True
                print(json.dumps(p.get_all_pathdata(),indent=2))
            if user_input=="P":
                valid_input = True
                print(json.dumps(p.get_all_path_data_params(),indent=2))
            if user_input=="m":
                valid_input = True
                print(json.dumps(p.get_path_methods(), indent=2))
            if user_input=="c":
                valid_input = True
                newfile=input("OpenAPI Filepath: ")
                OPENAPIFILE=newfile
                set_parser_OpenAPI_file()
            if user_input=='b':
                return
            if user_input=='h':
                valid_input = True
                print_parser_menu()
            if valid_input is False:
                print("No valid option!")
            valid_input=False
            user_input=""
            user_input = input()

    else:
        print("No OpenAPI specification file available.")
        return

# Report menu text generation and print to stdout
def print_server_menu():
    global SERVER, PORT
    menutext= "\n" \
              "Server base path: " + SERVER + " \t Port: "+PORT+"\n"  \
              "Server menu: \n" \
              "s: \t Set server base path \n" \
              "p: \t Set server port \n" \
              "h: \t Show this menu again \n" \
              "b: \t Go back"
    print (menutext)

# Function for control Server Submenu
def server_menu():
    global SERVER, PORT
    print_server_menu()
    state=True
    user_input = input()
    valid_input = False
    while state:
        if user_input=='s':
            valid_input = True
            newserver = input("New Server base path: ")
            SERVER=newserver
            print("New server base path set to: "+SERVER)
        if user_input=='p':
            valid_input=True
            newport = input("New Server Port: ")
            PORT = newport
            print("New server Port set to: " + PORT)
        if user_input=='b':
            return
        if user_input=='h':
            valid_input = True
            print_server_menu()
        if valid_input is False:
            print("No valid option!")
        valid_input=False
        user_input=""
        user_input = input()


# Report menu text generation and print to stdout
def print_report_menu():
    if write_report:
        reportstatus="Enabled"
    else:
        reportstatus = "Disabled"
    menutext = "\n" \
               "Report Menu: \n" \
               "f: \t Change filename. Filename: "+ reportfile + "\n" \
               "r: \t Enable/Disable report generation. Status: "+ reportstatus +" \n" \
               "h: \t Show this menu again \n" \
               "b: \t Go back"
    print (menutext)

# Function for control Report Submenu
def report_menu():
    global reportfile, write_report, report
    print_report_menu()
    sel_option = input()
    valid_input=False
    while True:
        if sel_option == "f":
            valid_input=True
            new_filename=input("New filename: ")
            reportfile=new_filename
            report=Report(reportfile)
            print_report_menu()
        if sel_option == "h":
            valid_input = True
            print_report_menu()
        if sel_option == "b":
            return
        if sel_option == "r":
            valid_input = True
            if write_report:
                write_report = False
            else:
                write_report = True
            print_report_menu()
        if valid_input is False:
            print("No valid option!")

        valid_input = False
        sel_option = ""
        sel_option = input()


# Function for control Main menu
def main_menu():
    print_main_menu()
    sel_option = input()
    valid_input = False
    while True:
        if sel_option == "m":
            valid_input = True
            module_menu()
            print_main_menu()
        if sel_option == "p":
            valid_input = True
            parser_menu()
            print_main_menu()
        if sel_option == "h":
            valid_input = True
            print_main_menu()
        if sel_option == "s":
            valid_input = True
            server_menu()
            print_main_menu()
        if sel_option == "q":
            exit(0)
        if sel_option == "r":
            valid_input = True
            report_menu()
            print_main_menu()
        if valid_input is False:
            print("No valid option!")
        valid_input = False
        sel_option = ""
        sel_option = input()

# Main method: is the programs start function and opens the main menu function
def main():
    check_modules()

    if OPENAPIFILE != "":
        set_parser_OpenAPI_file()
    if AUTO:
        module_names=AUTO_MODULES.split(";")
        selected=get_number_to_modulename(module_names)

        if len(selected)!=0:
            run_modules(selected)
        else:
            exit("Automation mode failed: No available modules detected!")
    else:
        print(programinfo)
        main_menu()

class MainClass():
    from __main__ import SERVER,PORT


# Will be exectuded if the main.py file is opened. Starts the main() function.
if __name__ == '__main__':
    main()










