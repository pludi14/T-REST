import json


class Parser:

    def __init__(self, file):
        self.__file = file
        self.__paths = {}
        self.parse_file()

    def __str__(self):
        return str(self.__data)

    def parse_file(self):
        with open(file=self.__file, encoding="UTF-8") as f:
            data = json.loads(f.read())
            self.__data = data
            # print(self.__data)

    # Returns all URIs
    def get_all_paths(self):
        paths = self.__data.get("paths").keys()
        paths = list(paths)

        self.__paths = paths
        return self.__paths
