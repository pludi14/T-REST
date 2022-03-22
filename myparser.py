import json
import logging


class Parser:

    def __init__(self, file):
        self.__file = file
        self.__paths = {}
        self.__servers=[]
        self.parse_file()

    def __str__(self):
        return str(self.data)

    def parse_file(self):
        try:
            with open(file=self.__file, encoding="UTF-8") as f:
                data = json.loads(f.read())
                self.data = data
                self.paths = self.data.get("paths")
        except Exception as e:
            print("File cannot be opened: "+ str(e))

    # Returns all URIs
    def get_all_paths(self):
        paths = self.data.get("paths").keys()
        paths = list(paths)

        self.__paths = paths
        return self.__paths

    def get_path_methods(self):
        pathdata={}
        paths = self.data.get("paths")

        for path, methods in paths.items():
            pathdata[path]=list(methods.keys())
            #for method in methods.items():
            #    print(method)
                #data_mathods.append(method)

        return pathdata

    def get_all_pathdata(self):
        all_pathdata=self.paths
        return all_pathdata

    def get_pathdata(self, path):
        pathdata=self.paths[path]
        return pathdata

    def get_servers(self):
        self.__servers=[]
        try:
            servers=self.data.get("servers")
            for url in servers:
                self.__servers.append(url.get("url"))
            return self.__servers
        except:
            #Muss Log Nachricht ausgeben
            print("No Server in description file")
            return False




