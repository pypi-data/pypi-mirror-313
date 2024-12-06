import json
from ..config import RobloxAPIConfig as config
from datetime import datetime

class DataStoreEntry:
    def __init__(self, key : str, value : object, createTime : datetime, revisionCreateTime : datetime):
        self.key : str = key
        self.value : object = value
        self.createTime : datetime = createTime
        self.revisionCreateTime : datetime = revisionCreateTime
    def toJson(self, convert : bool = False):
        val = {"key" : self.key, "value" : self.value}
        if convert:
            return json.dumps(val)
        return val
    def __str__(self):
        return f"Entry(key={self.key}, value={self.value})"

class DataStore:
    def __init__(self, api, name):
        self.api = api
        self.name = name
    def GetEntry(self, key):
        if not self.api.check_auth():
            return 
        result = self.api.request(config.ENTRYURL.format(universeid=self.api.universeId, datastore=self.name, entry=key),
                                  {"x-api-key" : self.api.api_key}, {})
        status_code = result.status_code
        if status_code != 200:
            return 
        result_data = json.loads(result.content)
        
        return DataStoreEntry(result_data["id"], result_data["value"], DataStore.loadTime(result_data["createTime"]), DataStore.loadTime(result_data["revisionCreateTime"]))
    
    def SetEntry(self, key : str, value : object):
        if not self.api.check_auth():
            return 
        data = {
            "value": value,
        }
        data = json.dumps(data)
        result = self.api.post(config.ENTRIESURL.format(universeid=self.api.universeId, datastore=self.name),
                                  {"x-api-key" : self.api.api_key, "content-type" : "application/json"}, {"id" : key}, data=data)
        status_code = result.status_code
        if status_code == 400:
            result = self.api.patch(config.ENTRYURL.format(universeid=self.api.universeId, datastore=self.name, entry=key),
                                    {"x-api-key" : self.api.api_key, "content-type" : "application/json"}, {"id" : key}, data=data)
        result_data = json.loads(result.content)
        return result_data
        
    def IncrementEntry(self, key : str, amount : int):
        if not self.api.check_auth():
            return 
        data = {
            "amount": amount,
        }
        data = json.dumps(data)
        result = self.api.post(config.ENTRYINCREMENTURL.format(universeid=self.api.universeId, datastore=self.name, entry=key),
                            {"x-api-key" : self.api.api_key, "content-type" : "application/json"}, {}, data=data)
        status_code = result.status_code
        result_data = json.loads(result.content)
        return result_data
    
    def DeleteEntry(self, key : str):
        if not self.api.check_auth():
            return 
        result = self.api.delete(config.ENTRYURL.format(universeid=self.api.universeId, datastore=self.name, entry=key),
                                 {"x-api-key" : self.api.api_key}, {})
        status_code = result.status_code
        result_data = json.loads(result.content)
        return result_data
    
    
    def ListEntries(self, temp_result = None, nextPageToken = ""):
        if not self.api.check_auth():
            return
        
        if temp_result is None:
            temp_result = []    
    
        result = self.api.request(config.ENTRIESURL.format(universeid=self.api.universeId, datastore=self.name),
                              {"x-api-key" : self.api.api_key}, {"pageToken" : nextPageToken, "maxPageSize" : 2})
        status_code = result.status_code
        if status_code != 200:
            return temp_result
        result_data = json.loads(result.content)
        keys = list(result_data.keys())
        if "dataStoreEntries" not in keys:
            return temp_result
        data = result_data["dataStoreEntries"]
        for e in data:
            entry = self.GetEntry(e["id"])
            temp_result.append(entry)
        if "nextPageToken" in list(result_data.keys()):
            nextPageToken = result_data["nextPageToken"]
        else:
            nextPageToken = ""
        if nextPageToken == "" or nextPageToken == None:
            result = temp_result
            temp_result = []
            return result
        else:
            return self.ListEntries(temp_result=temp_result, nextPageToken=nextPageToken)
        
    @staticmethod
    def loadTime(string : str):
        if(string.count("0") > 0):
            for i in range(0, string.count("0")):
                string.replace("0", "0o")
        index = string.find(".")
        if index > -1:
            string = string[:index]
        time = datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")
        return time        
    
    def __str__(self):
        return f"DataStore({self.api.universeId}, {self.name})"

