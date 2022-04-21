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
            logging.exception(e)

    # Returns all URIs
    def get_all_paths(self):
        paths = self.data.get("paths").keys()
        paths = list(paths)

        self.__paths = paths
        return self.__paths

    #Not used.
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

    #Not used.
    def get_pathdata(self, path):
        pathdata=self.paths[path]
        return pathdata

    def get_all_path_data_params(self):
        pathsdata={}
        for path, data in self.paths.items():
            pathsdata[path]={}
            for method, methoddata in data.items():
                if method=="get":
                    pathsdata[path].update({"get":None})

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

    def get_parameters_from_schema(self, schemaobject):
        params={}
        schemapath=schemaobject.split("/")
        schemapath.remove("#")
        schemadata = self.data
        for i in range(len(schemapath)):
            schemadata=schemadata.get(schemapath[i])
            i=i+1
        properties=schemadata.get("properties")
        for poperty, data in properties.items():
            params.update({data["title"]:data["type"]})
        return params



    def get_servers(self):
        self.__servers=[]
        try:
            servers=self.data.get("servers")
            for url in servers:
                self.__servers.append(url.get("url"))
            return self.__servers
        except:
            logging.exception("No Server in description file")
            return False






