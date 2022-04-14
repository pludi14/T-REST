import random
import requests


class Testgenerator():
    def __init__(self, url, port):
        self.url = url
        self.port= port


    def check_request(self, pathdata, path):
        for method, methoddata in pathdata.items():
            requestparams=self.create_request_data(methoddata["parameters"])

            URL=self.url+path

            if method == "get":

                r=requests.get(URL, params=requestparams)
                print(r.text)

    def check_response(self):
        pass

    def check_https(self):

        pass

    #Creates the Data that is transmitted in a Request
    def create_request_data(self, parameters):
        data={}
        for parameter in parameters:
            param_in=parameter["in"]
            name = parameter["name"]
            required=parameter["required"]
            schema=parameter["schema"]

            match param_in:
                case "query":
                    params={}
                    params[name]=self.generate_inputvalue(schema)
                    #data["params"]=params
                case "header":
                    #do something
                    pass

                case "path":
                    # put params in qery (body)
                    pass

                case "cookie":
                    # do something
                    pass
        return params


    #generates Random Values
    def generate_inputvalue(self, schema):

        type=schema["type"]
        format=schema["format"]

        match type:
            case "integer":
                value=random(1,20000)

            case "string":
                random_string = ""

                for _ in range(100):
                    # Considering only upper and lowercase letters
                    random_integer = random.randint(97, 97 + 26 - 1)
                    flip_bit = random.randint(0, 1)
                    # Convert to lowercase if the flip bit is on
                    random_integer = random_integer - 32 if flip_bit == 1 else random_integer
                    # Keep appending random characters using chr(x)
                    random_string += (chr(random_integer))
                value=random_string

        return value


    def try_dos(self):
        pass

