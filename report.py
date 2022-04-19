import os.path

import logging
from datetime import datetime


class Report():

    def __init__(self, path):
        self.reportfile=path
        self.check_file()

    def check_file(self):
        if os.path.exists(self.reportfile):
            now = datetime.now()
            current_time = now.strftime("%H_%M_%S")
            self.reportfile=self.reportfile+"_"+current_time

    def add_module_report(self, modreport, modname):
        with open(self.reportfile,"a") as f:
            f.write("Report of Module "+modname+": \n")
            f.write(modreport)

    def add_module_exception_report(self, exception, modname):
        with open(self.reportfile,"a") as f:
            f.write("An error occurred during the execution of the module "+modname+": \n")
            f.write("\t"+str(exception))





    