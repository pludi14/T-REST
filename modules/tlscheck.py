import json
import socket
import ssl
import certifi
import urllib.parse

#Import TREST Framework Methods and Attributes
import requests

from main import TREST_Framework
trest=TREST_Framework()

url=trest.get_server()
port=trest.get_port()

class TLSCheckerException(Exception):
    pass

def get_hostname_from_url(url):
    parsed_url=urllib.parse.urlparse(url)
    return parsed_url.netloc

def is_https():
    ishttps=False
    parsed_url = urllib.parse.urlparse(url)

    if parsed_url.scheme=="https":
        ishttps=True
    return ishttps

def get_context():
    context = ssl.create_default_context()
    context.check_hostname=False
    context.verify_mode=ssl.CERT_NONE
    return context

def get_default_cipherlist(context):
    defaultcipherlist=[]
    defaultciphers=context.get_ciphers()
    for cipher in defaultciphers:
        defaultcipherlist.append(cipher["name"])
    return defaultcipherlist

# checks for Ciphers that are declared as Medium secure from OpenSSL
def check_medium_ciphers(context, defaultcipherlist):
    sharedcipherlist=[]
    context=context
    context.set_ciphers("MEDIUM")
    mediumciphers=context.get_ciphers()
    mediumcipherlist=[]
    for cipher in mediumciphers:
        mediumcipherlist.append(cipher["name"])
    try:
        with socket.create_connection((url, port),3) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                shared_ciphers=ssock.shared_ciphers()
                sharedcipherlist=[]
                for cipher in shared_ciphers:
                    sharedcipherlist.append(cipher[0])

        for c in set(defaultcipherlist) & set(mediumcipherlist):
            sharedcipherlist.remove(c)
    except Exception as e:
        raise TLSCheckerException("Check Medium Cipher Error: "+str(e))
    return sharedcipherlist

# def check_cypher_suites(context):
#     insecure_list=[]
#     insecure_res=requests.get("https://ciphersuite.info/api/cs/security/insecure/")
#     insecuredict=json.loads(insecure_res.text)
#
#     weak_list=[]
#     weak_res=requests.get("https://ciphersuite.info/api/cs/security/weak/")
#     weakdict = json.loads(weak_res.text)
#
#     for cipherdict in insecuredict["ciphersuites"]:
#         for cipher in cipherdict.keys():
#             insecure_list.append(cipher)
#
#     for cipherdict in weakdict["ciphersuites"]:
#         for cipher in cipherdict.keys():
#             weak_list.append(cipher)
#
#
#     context = context
#     for cipher in weak_list:
#         try:
#             print("TLS_AES_128_GCM_SHA256")
#             context.set_ciphers("TLS_AES_128_GCM_SHA256")
#             with socket.create_connection((url, port), 3) as sock:
#                 with context.wrap_socket(sock, server_hostname=url) as ssock:
#                     print("Worked")
#         except Exception as e:
#             print("ERROR" + str(e))
#             continue


# Returns a Dict with server certificate information
#{ "verified":True/False,
# "peercert": dict with peer cert information or None
# "error message": Message of Exception if verfifcation failed}
def check_certificate(context):
    verification_information={}

    context.check_hostname=True
    context.verify_mode=ssl.CERT_REQUIRED
    context.load_verify_locations(certifi.where())
    try:
        with socket.create_connection((url, port),3) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                server_cert=ssock.getpeercert()
                verification_information["verified"]=True
                verification_information["peercert"]=server_cert
    except TimeoutError as e:
        raise TLSCheckerException("Check Certificate Error:"+str(e))
        verification_information["verified"] = False
        verification_information["peercert"] = None
        verification_information["error message"] = error_message

    except ssl.SSLCertVerificationError as e:
        error_message = str(e)
        verification_information["verified"] = False
        verification_information["error message"] = error_message
        verification_information["peercert"] = get_cert_info_without_verification(context)

    except Exception as e:
        raise TLSCheckerException("Check Certificate Error:" + str(e))
        verification_information["verified"] = False
        verification_information["error message"] = error_message
        verification_information["peercert"]=None

    return verification_information

# Returns Server Certificate Information without Verification
def get_cert_info_without_verification(context):
    context.check_hostname=False
    context.verify_mode=ssl.CERT_NONE
    server_cert={}

    try:
        with socket.create_connection((url, port),3) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                print(ssock.getpeercert())
                server_cert=ssock.getpeercert()
    except Exception as e:
        raise TLSCheckerException("Get Cert Info without Verification Error:" + str(e))
    return server_cert

def run():
    global url
    report=""
    if not is_https():
        raise TLSCheckerException("The Server does not support https. No https in given URL.")
        return "The Server does not support https. No https in given URL."
    url=get_hostname_from_url(url)

    reportlist=[]

    try:
        context = get_context()
        defaultcipherlist = get_default_cipherlist(context)
        result=check_medium_ciphers(context, defaultcipherlist)
        check_cypher_suites(context)
        if len(result)!=0:
            reportlist.append("The following medium secure declared cypher suites are supported: \n" + str(result))
        else:
            reportlist.append("The server does not accept any medium secure cipher suites.")

        verification_info=check_certificate(context)
        reportlist.append("Verification Information: \n"+str(json.dumps(verification_info, indent=2)))

    except TLSCheckerException as e:
        raise TLSCheckerException("Error in run() method: "+str(e))

    return reportlist















