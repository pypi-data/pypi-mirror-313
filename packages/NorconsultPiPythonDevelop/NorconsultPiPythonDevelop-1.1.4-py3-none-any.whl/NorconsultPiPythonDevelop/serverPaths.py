import msal
import os
import atexit
import logging
import requests
logging.captureWarnings(True)

class Authenticate: 
    def __init__(self):
        self.authority = "https://login.microsoftonline.com/ce25ca93-004f-44f4-a6b5-eb22b45815aa"
        self.client_id = "6f8f2901-7ae6-42bd-9239-0f1e0d43856f"
        self.scope = ["api://6f8f2901-7ae6-42bd-9239-0f1e0d43856f/access_as_user"]

    def get_access_token(self):
        config = {
        "authority": "https://login.microsoftonline.com/ce25ca93-004f-44f4-a6b5-eb22b45815aa",
        "client_id": "6f8f2901-7ae6-42bd-9239-0f1e0d43856f",
        "scope": ["api://6f8f2901-7ae6-42bd-9239-0f1e0d43856f/access_as_user"],
        }

        cache = msal.SerializableTokenCache()

        if os.path.exists("token_cache.bin"):
            cache.deserialize(open("token_cache.bin", "r").read())
        
        atexit.register(lambda: open("token_cache.bin", "w").write(cache.serialize()) if cache.has_state_changed else None)

        # Create a preferably long-lived app instance which maintains a token cache.
        app = msal.PublicClientApplication(self.client_id, authority = self.authority, token_cache = cache)

        accounts = app.get_accounts()
        result = app.acquire_token_silent(self.scope, account = None if not accounts else accounts[0])

        if not result: 
           result = app.acquire_token_interactive(self.scope)
           return result["access_token"]

        elif "access_token" in result:
            access_token = result["access_token"]
            return access_token
        else: 
            print('Failed')
            return None

class Request: 
    def __init__(self, access_token):
        self.headers = headers = {'Accept': 'accept: text/plain',
                                  'authorization': 'Bearer ' + access_token}

    def get(self, request_uri, ploads):
        response = requests.get(request_uri, headers = self.headers, params = ploads, verify = False)
        return response
    
class RouteBuilder: 

    def __init__(self, Controller): 
        SchemaName = 'common'
        self.RequestURI = 'https://u-pi-db-' + SchemaName + '.norconsult.com/api/' + SchemaName + '/' + Controller + '/'

    def GetRoute(self, ControllerName):
        return self.RequestURI + ControllerName

def getServerPaths():
    access_token = Authenticate().get_access_token()
    routeBuilder = RouteBuilder("ServerPath")
    piRequest = Request(access_token)
    try: 
        response = piRequest.get(request_uri = routeBuilder.GetRoute("GetServerPathsDevelop"), ploads = {})
    except: 
        print("Unable to retrieve server path to fetch newest client files. Please ensure that you are connected to the Norconsult VPN.")
        return
    try: 
        return response.json()
    except: 
        print("Could not fetch server adresses. Status code: " + str(response.status_code))
        return
