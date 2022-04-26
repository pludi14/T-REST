"""
T-REST: Report generation class for T-REST by @MarcelPludra
"""

import os.path

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

    #Writes the report file. modreport = List with report text. 1 text line=1list value.
    def add_module_report(self, modreport, modname):
        with open(self.reportfile,"a") as f:
            f.write("Report of Module "+modname+": \n")
            for line in modreport:
                f.write(line+"\n")
            f.write("\n ---------------------End of Module Report---------------------------- \n \n")
        f.close()

    def add_module_exception_report(self, exception, modname):
        with open(self.reportfile,"a") as f:
            f.write("An error occurred during the execution of the module "+modname+": \n")
            f.write("\t"+str(exception))
            f.write("\n ---------------------End of Module Report---------------------------- \n \n")
        f.close()





    