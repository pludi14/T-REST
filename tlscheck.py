import socket
import ssl
import logging
import certifi
from setup_logger import logger

# Setup Logging
logger = logging.getLogger("tlscheck")

class TLScheck():


    def __init__(self, url, port):
        self.url = url
        self.port= port
        self.context=self.get_context()
        self.defaultcipherlist=self.get_default_cipherlist(self.context)

    def get_context(self):
        context = ssl.create_default_context()
        context.check_hostname=False
        context.verify_mode=ssl.CERT_NONE
        return context

    def get_default_cipherlist(self, context):
        defaultcipherlist=[]
        defaultciphers=context.get_ciphers()
        for cipher in defaultciphers:
            defaultcipherlist.append(cipher["name"])
        return defaultcipherlist

    # checks for Ciphers that are declared as Medium secure from OpenSSL
    def check_medium_ciphers(self):
        sharedcipherlist=[]
        context=self.context
        context.set_ciphers("MEDIUM")
        mediumciphers=context.get_ciphers()
        mediumcipherlist=[]
        for cipher in mediumciphers:
            mediumcipherlist.append(cipher["name"])

        try:
            with socket.create_connection((self.url, self.port),3) as sock:
                with context.wrap_socket(sock, server_hostname=self.url) as ssock:
                    shared_ciphers=ssock.shared_ciphers()
                    sharedcipherlist=[]
                    for cipher in shared_ciphers:
                        sharedcipherlist.append(cipher[0])

            for c in set(self.defaultcipherlist) & set(mediumcipherlist):
                sharedcipherlist.remove(c)
        except Exception as e:
            logger.exception(e)
            print("Socket creation failure: "+str(e))
        return sharedcipherlist


    # Returns a Dict with server certificate information
    #{ "verified":True/False,
    # "peercert": dict with peer cert information or None
    # "error message": Message of Exception if verfifcation failed}
    def check_certificate(self):
        verification_information={}

        context=self.context
        context.check_hostname=True
        context.verify_mode=ssl.CERT_REQUIRED
        context.load_verify_locations(certifi.where())


        try:
            with socket.create_connection((self.url, self.port),3) as sock:
                with context.wrap_socket(sock, server_hostname=self.url) as ssock:
                    server_cert=ssock.getpeercert()
                    verification_information["verified"]=True
                    verification_information["peercert"]=server_cert
        except TimeoutError as e:
            logger.exception(e)
            error_message=str(e)
            verification_information["verified"] = False
            verification_information["peercert"] = None
            verification_information["error message"] = error_message
            print("Certifcate Verfication Failure: " + error_message)
        except OSError as e:
            logger.exception(e)
            error_message = str(e)
            verification_information["verified"] = False
            verification_information["error message"] = error_message
            verification_information["peercert"]=None
            print("Certifcate Verfication Failure: " + error_message)
        except ssl.SSLCertVerificationError as e:
            logger.exception(e)
            error_message = str(e)
            verification_information["verified"] = False
            verification_information["error message"] = error_message
            verification_information["peercert"] = self.get_cert_info_without_verification()
            print("Certifcate Verfication Failure: " + error_message)

        return verification_information

    # Returns Server Certificate Information without Verification
    def get_cert_info_without_verification(self):
        context = self.context
        context.check_hostname=False
        context.verify_mode=ssl.CERT_NONE
        server_cert={}

        try:
            with socket.create_connection((self.url, self.port),3) as sock:
                with context.wrap_socket(sock, server_hostname=self.url) as ssock:
                    server_cert=ssock.getpeercert()
        except Exception as e:
            logger.exception(e)
        return server_cert






