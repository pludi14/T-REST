"""
T-REST: OpenAPI Parser class for T-REST by @MarcelPludra
"""

import json

class Parser:

    def __init__(self):
        self.__file = ""
        self.__paths = {}
        self.__servers=[]

    def __str__(self):
        return str(self.data)

    # Set OpenAPI Specification file
    def setFile(self, file):
        self.__file = ""
        self.__paths = {}
        self.__servers=[]
        self.__file=file
        self.parse_file()

    # Parses the OpenAPI Specification file
    def parse_file(self):
        try:
            with open(file=self.__file, encoding="UTF-8") as f:
                data = json.loads(f.read())
                self.data = data
                self.paths = self.data.get("paths")
        except Exception as e:
            print("parse_file: Error in parsing the OpenAPI specification file!")

    # Returns all URIs
    def get_all_paths(self):
        paths = self.data.get("paths").keys()
        paths = list(paths)

        self.__paths = paths
        return self.__paths

    # Returns all paths with respective methods
    def get_path_methods(self):
        pathdata={}
        paths = self.data.get("paths")

        for path, methods in paths.items():
            pathdata[path]=list(methods.keys())
        return pathdata

    #Returns all paths and respective data
    def get_all_pathdata(self):
        all_pathdata=self.paths
        return all_pathdata

    # Returns all path data from a specific path
    def get_pathdata(self, path):
        pathdata=self.paths[path]
        return pathdata

    # Returns all data from every path available as a dict
    def get_all_path_data_params(self):
        pathsdata={}
        for path, data in self.paths.items():
            pathsdata[path]={}
            for method, methoddata in data.items():
                if method=="get":
                    pathsdata[path].update({"get":None})
                    # Not finished
                if method=="head":
                    pathsdata[path].update({"head":None})
                if method=="post":
                    rbody=methoddata.get("requestBody")
                    schema=rbody["content"]["application/json"].get("schema")
                    if "$ref" in schema.keys():
                        ref=schema["$ref"]
                        params=self.get_parameters_from_schema(ref)
                        pathsdata[path].update({"post":params})
        return pathsdata

    # For internal use. Gets parameter from schema object in OpenAPI specification file
    def get_parameters_from_schema(self, schemaobject):
        params={}
        try:
            schemapath=schemaobject.split("/")
            schemapath.remove("#")
            schemadata = self.data
            for i in range(len(schemapath)):
                schemadata=schemadata.get(schemapath[i])
                i=i+1
            properties=schemadata.get("properties")
            for poperty, data in properties.items():
                params.update({data["title"]:data["type"]})
        except Exception as e:
            print("Error in parsing parameters from schema data: "+str(e))
            return params
        return params

    # Returns Server from OpenAPI specification file
    def get_servers(self):
        self.__servers=[]
        try:
            servers=self.data.get("servers")
            for url in servers:
                self.__servers.append(url.get("url"))
            return self.__servers
        except:
            print("No server in OpenAPI specification file.")
            return False






