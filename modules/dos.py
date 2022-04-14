import asyncio
import concurrent.futures
import requests

# Number of concurrent Requests
nr_of_threads=12
nr_of_parallel_requests=3

# Import TREST Framework Methods and Attributes
from main import TREST_Framework
trest=TREST_Framework()

url=trest.get_server()
port=trest.get_port()
protocol=trest.get_protocol()
hostname=trest.get_hostname()
pathsdata=trest.get_all_path_info()

responses=[]

# Prepare the data needed for Requets (Parameters, etc.)
def prepare_requests():
    getUrls = {}
    postUrls = {}
    headUrls= {}
    for path,methods in pathsdata.items():
        for method,params in methods.items():
            if method=="get":
                params={}
                getUrls[protocol+"://"+hostname+":"+port+path]=params

            if method=="post":
                for key, value in params.items():
                    if value =="string":
                        params.update({key: trest.get_random_string(20)})
                    if value=="integer":
                        params.update({key: trest.get_random_integer(100,1000)})

                    data=params
                    postUrls[protocol + "://" + hostname + ":" + port + path]=data

            if method=="head":
                params = {}
                headUrls[protocol+"://"+hostname+":"+port+path]=params
    return (getUrls, postUrls, headUrls)


# Build requests and send to server: Return = Response
# data = In Body
# params = URL
def create_Request(path, method, queryParameter=None, querryData=None):
    apiUrl = path
    #print(path, method, querryData)

    if method=="GET":
        response = requests.get(url=apiUrl, params=queryParameter)

    if method=="PUT":
        response = requests.put(url=apiUrl, params=queryParameter, data=querryData)

    if method=="POST":
        response = requests.post(url=apiUrl, params=queryParameter, data=querryData)

    if method=="DELETE":
        response = requests.delete(url=apiUrl, params=queryParameter)

    return response


def send_POST(*args, **kwargs):
    print(args)
    print(kwargs)
    # for key, value in kwargs.items():
    #     print(key, value)

async def run_dos(datapack):
    print(datapack)
    with concurrent.futures.ThreadPoolExecutor(max_workers=nr_of_threads) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, create_Request, (*datapack,  )) for i in range(nr_of_parallel_requests)
        ]
        for response in await asyncio.gather(*futures):
            responses.append(response)

def check_responses(responses):
    for r in responses:
        print(r.status_code)
        print(r.reason)
        print(r.elapsed)



def run():

    getUrls,postUrls,headUrls=prepare_requests()
    loop = asyncio.new_event_loop()

    # if len(headUrls) != 0:
    #     for url in headUrls:
    #         loop.run_until_complete(run_dos((url, "GET")))
    # if len(getUrls) != 0:
    #     for url in getUrls:
    #         loop.run_until_complete(run_dos((url, "GET")))

    if len(postUrls) != 0:
        for url,data in postUrls.items():
            send_POST(url, "POST", **data)
            #loop.run_until_complete(run_dos((url, "POST")))

    check_responses(responses)
    loop.close()
    pass
