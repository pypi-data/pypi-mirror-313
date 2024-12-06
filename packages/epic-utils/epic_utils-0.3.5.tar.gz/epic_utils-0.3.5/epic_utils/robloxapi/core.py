import requests
import json
from ..config import RobloxAPIConfig as config
from .datastore import DataStore, DataStoreEntry

class RequestNotAuthorized(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class APIConnection:
    def __init__(self, universeId):
        self.universeId = universeId    
    
    def check_auth(self):
        keys = list(self.__dict__.keys())
        
        if "api_key" not in keys:
            raise RequestNotAuthorized("API Connection wasnt authorized")
        return True
        
    def auth(self, api_key):
        self.api_key = api_key
        try:
            self.universeData = self.GetData()
            self.universeName = self.universeData["displayName"]
            self.universeDescription = self.universeData["description"]
            self.universeVisiblity = self.universeData["visibility"]
            self.universeGroup = self.universeData["group"]
        except Exception as error:
            return False
        return True
    def ListDataStores(self, temp_result = None, nextPageToken=""):
        if not self.check_auth():
            return
        
        if temp_result is None:
            temp_result = []
            
        result = self.request(config.DATASTOREURL.format(universeid=self.universeId),
                              {"x-api-key" : self.api_key}, {"pageToken" : nextPageToken, "maxPageSize" : config.PAGESIZE})
        status_code = result.status_code
        if status_code != 200:
            return temp_result
        result_data = json.loads(result.content)
        data = result_data["dataStores"]
        for ds in data:
            ds = DataStore(self, ds["id"])
            temp_result.append(ds)
        if "nextPageToken" in list(result_data.keys()):
            nextPageToken = result_data["nextPageToken"]
        else:
            nextPageToken = ""
        if nextPageToken == "" or nextPageToken == None:
            return temp_result
        else:
            return self.ListDataStore(temp_result=temp_result, nextPageToken=nextPageToken)
            
    def GetDataStore(self, datastore_name):
        return DataStore(self, datastore_name)
    
    def GetData(self):
        result = self.request(config.UNIVERSEURL.format(universeid=self.universeId),
                              {"x-api-key" : self.api_key}, {})
        status_code = result.status_code
        if status_code != 200:
            return None
        result_data = json.loads(result.content)
        return result_data
    
    def restart(self):
        result = self.post(config.UNIVERSERESTARTURL.format(universeid=self.universeId),
                           {"x-api-key" : self.api_key}, {})
        status_code = result.status_code
        if status_code != 200:
            return False
        return True
    
    def request(self, url, headers, params, data={}):
        result = requests.get(url, params=params, headers=headers, data=data)
        return result
    def post(self, url, headers, params, data={}):
        result = requests.post(url, params=params, headers=headers, data=data)
        return result
    def delete(self, url, headers, params, data={}):
        result = requests.delete(url, params=params, headers=headers, data=data)
        return result
    def patch(self, url, headers, params, data={}):
        result = requests.patch(url, params=params, headers=headers, data=data)
        return result
