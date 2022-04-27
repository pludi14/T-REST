"""
T-REST - vulnscan.py: Vulnerability scan module by @MarcelPludra
"""
import json

import requests

class VulnScanException(Exception):
    pass

from trest import TREST_Framework
trest=TREST_Framework()

def get_Server_Version():
    try:
        r=requests.head(url=trest.get_server(), verify=False)
    except Exception as e:
        raise VulnScanException("Cannot connect to server! "+ str(e))

    server_header=r.headers["Server"]
    server=server_header.split(" ")[0].replace("/"," ")

    return server

def get_cvssv3_CRITICAL_CVEs(keyword):
    report_CRITICAL=["The following CVEs with a CRITICAL CVSS 3.x severity where found for the keyword "+ keyword + ": "]
    querryParams = {}
    querryParams["keyword"] = keyword
    querryParams["cvssV3Severity"] = "CRITICAL"
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0/"

    try:
        res = requests.get(url, params=querryParams)
    except Exception as e:
        raise VulnScanException("Cannot conenct to NATIONAL VULNERABILITY DATABASE API: "+str(e))

    if res.status_code==200:
        result=json.loads(res.text)
        search_results=result["result"]
        if result["totalResults"]>0:
            for cve in search_results["CVE_Items"]:
                cve_ID=cve["cve"]["CVE_data_meta"]["ID"]
                cve_publish_date=cve["publishedDate"]
                cve_description=cve["cve"]["description"]["description_data"][0]["value"]
                cve_URL="https://nvd.nist.gov/vuln/detail/"+cve_ID
                report_CRITICAL.append(cve_ID+" - "+cve_publish_date+ " - "+cve_URL)
                report_CRITICAL.append("\t"+cve_description)
            return report_CRITICAL
        else:
            return ["No CVEs with a CRITICAL CVSS 3.x severity where found for the keyword: "+ keyword]
    else:
        return ["Failure in NATIONAL VULNERABILITY DATABASE API request: "+str(res.status_code) + ": " + res.reason]

def get_cvssv3_HIGH_CVEs(keyword):
    report_CRITICAL=["The following CVEs with a HIGH CVSS 3.x severity where found for the keyword "+ keyword + ": "]
    querryParams = {}
    querryParams["keyword"] = keyword
    querryParams["cvssV3Severity"] = "HIGH"
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0/"

    try:
        res = requests.get(url, params=querryParams)
    except Exception as e:
        raise VulnScanException("Cannot conenct to NATIONAL VULNERABILITY DATABASE API: " + str(e))

    if res.status_code==200:
        result=json.loads(res.text)
        search_results=result["result"]
        if result["totalResults"]>0:
            for cve in search_results["CVE_Items"]:
                cve_ID=cve["cve"]["CVE_data_meta"]["ID"]
                cve_publish_date=cve["publishedDate"]
                cve_description=cve["cve"]["description"]["description_data"][0]["value"]
                cve_URL="https://nvd.nist.gov/vuln/detail/"+cve_ID
                report_CRITICAL.append(cve_ID+" - "+cve_publish_date+ " - "+cve_URL)
                report_CRITICAL.append("\t"+cve_description)
            return report_CRITICAL
        else:
            return ["No CVEs with a HIGH CVSS 3.x severity where found for the keyword: "+ keyword]
    else:
        return ["Failure in NATIONAL VULNERABILITY DATABASE API request: " + str(res.status_code) + ": " + res.reason]

def run():
    report=[]
    report.append("\n")
    try:
        for line in get_cvssv3_CRITICAL_CVEs(get_Server_Version()):
            report.append(line)
        report.append("\n")
        for line in get_cvssv3_HIGH_CVEs(get_Server_Version()):
            report.append(line)
        report.append("\n")
    except Exception as e:
        raise VulnScanException(str(e))
    return report