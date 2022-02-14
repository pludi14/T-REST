import json


class Parser:

    def __init__(self, file):
        self.__file= file
        self.parse_file()

    def __str__(self):
        return str(self.__data)


    def parse_file(self):
        with open(file=self.__file) as f:
            data = json.loads(f.read())
            self.__data=data
            #print(self.__data)








