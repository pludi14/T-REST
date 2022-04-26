"""
T-REST - dos.py: DoS module by @MarcelPludra
"""

import asyncio
import concurrent.futures
import datetime

import requests

class DosException(Exception):
    pass
# Number of concurrent Requests
nr_of_threads=3
nr_of_parallel_requests=2

# Import TREST Framework Class
from trest import TREST_Framework
trest=TREST_Framework()

url=trest.get_server()
port=trest.get_port()
protocol=trest.get_protocol()
hostname=trest.get_hostname()
pathsdata=trest.get_all_path_info()

responses=[]
report=[]

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
#path, method, queryParameter=None, querryData=None
def create_Request(datapack):
    apiUrl = datapack["url"]
    method = datapack["method"]
    queryParameter=None
    querryData=None
    if "queryParameter" in datapack:
        queryParameter=datapack["queryParameter"]
    if "querryData" in datapack:
        querryData=datapack["querryData"]
    try:
        if method=="HEAD":
            response = requests.head(url=apiUrl, params=queryParameter)

        if method=="GET":
            response = requests.get(url=apiUrl, params=queryParameter)

        if method=="PUT":
            response = requests.put(url=apiUrl, params=queryParameter, data=querryData)

        if method=="POST":
            response = requests.post(url=apiUrl, params=queryParameter, data=querryData)

        if method=="DELETE":
            response = requests.delete(url=apiUrl, params=queryParameter)

    except Exception as e:
        print("Failure in create_Request method of dos: " + str(e))

    return response



async def run_dos(datapack):
    with concurrent.futures.ThreadPoolExecutor(max_workers=nr_of_threads) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, create_Request, datapack) for i in range(nr_of_parallel_requests)
        ]
        for response in await asyncio.gather(*futures):
            responses.append(response)

def check_responses():
    global responses
    for r in responses:
        if r.status_code>=500:
            report.append("5XX status code response from: "+r.url +"\t Code:" +str(r.status_code)+"\t Reason:"+r.reason)
        if r.status_code>=400 and r.status_code<=499:
            report.append("4XX status code response from: "+r.url +"\t Code:" +str(r.status_code)+"\t Reason:"+r.reason)

        if r.elapsed > datetime.timedelta(seconds=2.0):
            report.append("Response time is > 2 seconds: "+r.url +"\t Code:" +str(r.status_code)+"\t Reason:"+r.reason)

def run():

    getUrls,postUrls,headUrls=prepare_requests()
    loop = asyncio.new_event_loop()

    try:
        if len(headUrls) != 0:
            for url in headUrls:
                datapack={}
                datapack["url"]=url
                datapack["method"] = "HEAD"
                loop.run_until_complete(run_dos(datapack))
        if len(getUrls) != 0:
            for url in getUrls:
                datapack={}
                datapack["url"]=url
                datapack["method"] = "GET"
                loop.run_until_complete(run_dos(datapack))

        if len(postUrls) != 0:
             for url,data in postUrls.items():
                 datapack = {}
                 datapack["url"] = url
                 datapack["method"] = "POST"
                 datapack["querryData"]=data
                 loop.run_until_complete(run_dos(datapack))
        check_responses()
    except Exception as e:
        raise DosException("Failure in run method of dos: " + str(e))
    loop.close()
    return report
