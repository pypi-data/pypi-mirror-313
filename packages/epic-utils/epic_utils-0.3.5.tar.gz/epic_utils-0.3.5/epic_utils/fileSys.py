import os
import json

class ReadError(Exception):
    def __init__(self, err_msg: str, file_path: str):
        self.message = f"Error occured while reading file ({file_path})\n{err_msg}"
    def __str__(self):
        return self.message

class WriteError(Exception):
    def __init__(self, err_msg: str, file_path: str):
        self.message = f"Error occured while writing file ({file_path})\n{err_msg}"
    def __str__(self):
        return self.message

class File:
    def __init__(self, path: str, create: bool = False):
        if (File.isAbsPath(path)):
            self.path = path
        else:
            self.path = File.toAbsPath(path)
        self.directory = File.directoryName(self.path)
        temp = File.splitExt(File.baseName(self.path))
        self.name = temp[0]
        self.extension = temp[1].lstrip(".")  
        print(self.name, self.extension)
        if create and not self.exists():
            self.create()
    @staticmethod
    def splitExt(path: str):
        return os.path.splitext(path)
    @staticmethod
    def baseName(path: str):
        return os.path.basename(path)
    @staticmethod
    def directoryName(path: str):
        return os.path.dirname(path) 
    @staticmethod
    def toAbsPath(path: str):
        return os.path.abspath(path)
    @staticmethod
    def isAbsPath(path: str):
        return os.path.isabs(path)
    @staticmethod
    def existsDir(path: str):
        return os.path.isdir(path)
    @staticmethod
    def listDir(directory: str):
        if not File.existsDir(directory):
            return []
        directory = directory if File.isAbsPath(directory) else File.toAbsPath(directory)
        return os.listdir(directory)
    def exists(self):
        return os.path.isfile(self.path)
    
    def create(self):
        with open(self.path, "x"):
            pass
    
    def update_path(self):
        _temp = File.splitExt(File.baseName(self.path))
        self.directory = os.path.dirname(self.path)
        self.file_name = _temp[0]
        self.file_extension = _temp[1]
    
    #reading and writing operations
    
    def write(self, data: str):
        try:
            with open(self.path, "w") as file:
                file.write(data)
        except Exception as error:
            raise WriteError(str(error), self.path)
        
    def read(self) -> str:
        try:
            with open(self.path, "r") as file:
                return file.read()
        except Exception as error:
            raise ReadError(str(error), self.path)

    def writeJSON(self, data: dict):
        try:
            str_data = json.dumps(data)
            self.write(str_data)
        except Exception as error:
            raise WriteError(str(error), self.path)

    def readJSON(self):
        str_data = self.read()
        try:
            data = json.loads(str_data)
            return data
        except Exception as error:
            raise ReadError(str(error), self.path)
        
    def delete(self):
        os.remove(self.path)
        del self

    def rename(self, name: str):
        new_path = f"{self.directory}/{name}.{self.file_extension}"
        os.rename(self.path, new_path)
        self.path = new_path
        self.update_path()
		
    def change_extension(self, extension: str):
        new_path = f"{self.directory}/{self.file_name}.{extension}"
        os.rename(self.path, new_path)
        self.path = new_path
        self.update_path()
        
class UserData:
    def __init__(self, path: str):
        self.file = File(path)
        self.data = {}
        
        self.load()
    
    def load(self):
        self.data = self.file.readJSON()
    
    def save(self):
        self.file.writeJSON(self.data)
        
    def setValue(self, key: str, value):
        self.data[key] = value
        self.save()
        
    def getValue(self, key: str):
        return self.data[key]
    
    def clear(self):
        self.data = {}
        self.save()
        
    def delete(self):
        self.file.delete()
        del self
    
        
class UserDataManager:
    def __init__(self, company_name: str, game_name: str):
        self.company_name = company_name
        self.game_name = game_name
        #check if directory exists in appdata, if not create it
        if not File.existsDir(f"{os.getenv('APPDATA')}/{company_name}"):
            os.mkdir(f"{os.getenv('APPDATA')}/{company_name}")
            
        if not File.existsDir(f"{os.getenv('APPDATA')}/{company_name}/{game_name}"):
            os.mkdir(f"{os.getenv('APPDATA')}/{company_name}/{game_name}")
            
        
        self.path = f"{os.getenv('APPDATA')}/{company_name}/{game_name}"
    def get(self, name: str):
        return UserData(f"{self.path}/{name}.json")
    