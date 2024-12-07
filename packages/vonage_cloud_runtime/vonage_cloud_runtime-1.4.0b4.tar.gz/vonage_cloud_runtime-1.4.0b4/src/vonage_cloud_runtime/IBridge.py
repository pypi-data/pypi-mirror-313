from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.request.contracts.IRequestParams import IRequestParams
from vonage_cloud_runtime.services.config.pathObject import PathObject
from vonage_cloud_runtime.errors.ISdkError import ISdkError
T = TypeVar('T')
K = TypeVar('K')

#interface
class IBridge(ABC):
    @abstractmethod
    def createSdkError(self,message: str):
        pass
    @abstractmethod
    def getErrorMessage(self,error: T):
        pass
    @abstractmethod
    def encodeUriComponent(self,s: str):
        pass
    @abstractmethod
    def parsePath(self,path: str):
        pass
    @abstractmethod
    def testRegEx(self,str: str,regExp: str):
        pass
    @abstractmethod
    def isInteger(self,value: int):
        pass
    @abstractmethod
    def substring(self,str: str,start: int,end: int = None):
        pass
    @abstractmethod
    def jsonStringify(self,data: object):
        pass
    @abstractmethod
    def jsonParse(self,json: str):
        pass
    @abstractmethod
    def getEnv(self,name: str):
        pass
    @abstractmethod
    def request(self,params: IRequestParams[T]):
        pass
    @abstractmethod
    def requestWithoutResponse(self,params: IRequestParams[T]):
        pass
    @abstractmethod
    def uuid(self):
        pass
    @abstractmethod
    def isoDate(self):
        pass
    @abstractmethod
    def runBackgroundTask(self,task: object):
        pass
    @abstractmethod
    def createReadStream(self,path: str):
        pass
    @abstractmethod
    def toISOString(self,seconds: int):
        pass
    @abstractmethod
    def jwtSign(self,payload: object,privateKey: str,alg: str,options: object = None):
        pass
    @abstractmethod
    def jwtVerify(self,token: str,privateKey: str,algorithm: str):
        pass
    @abstractmethod
    def jwtDecode(self,token: str):
        pass
    @abstractmethod
    def getSystemTime(self):
        pass
    @abstractmethod
    def log(self,data: object):
        pass
    @abstractmethod
    def getObjectKeys(self,obj: T):
        pass
    @abstractmethod
    def getValueAtPath(self,obj: T,path: List[object]):
        pass
    @abstractmethod
    def setValueAtPath(self,obj: T,path: List[object],value: object):
        pass
