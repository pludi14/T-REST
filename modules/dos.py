import asyncio
import concurrent.futures
import requests

# Number of concurrent Requests
nr_of_threads=100

#Import TREST Framework Methods and Attributes
from main import TREST_Framework
trest=TREST_Framework()

url=trest.get_server()
port=trest.get_port()
protocol=trest.get_protocol()
hostname=trest.get_hostname()
pathsdata=trest.get_all_path_info()


responses=[]

def create_requests():
    getUrls = []
    postUrls = []
    for path,methods in pathsdata.items():
        for method,params in methods.items():
            if method=="get":
                getUrls.append(protocol+"://"+hostname+":"+port+path)


    return (getUrls,postUrls)


#Requests werden hier zusammengebaut und an die Plattform gesendet.
def create_Request(path, method, queryParameter=None, querryData=None):
    apiUrl = path


    if method=="GET":
        response = requests.get(url=apiUrl, params=queryParameter)

    if method=="PUT":
        response = requests.put(url=apiUrl, params=queryParameter, data=querryData)

    if method=="POST":
        response = requests.post(url=apiUrl, params=queryParameter, data=querryData)

    if method=="DELETE":
        response = requests.delete(url=apiUrl, params=queryParameter)


    return response


async def run_dos(datapack):
    print(datapack)
    with concurrent.futures.ThreadPoolExecutor(max_workers=nr_of_threads) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, create_Request, *(datapack)) for i in range(100)
        ]
        for response in await asyncio.gather(*futures):
            responses.append(response)



def run():
    getUrls,postUrls=create_requests()
    loop = asyncio.new_event_loop()
    for url in getUrls:
        loop.run_until_complete(run_dos((url, "GET")))
    print(responses)
    loop.close()
    #print(pathsdata)


    pass