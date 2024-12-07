from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.contracts.fullText.createIndexOptions import CreateIndexOptions
from vonage_cloud_runtime.providers.state.enums.expireOption import EXPIRE_OPTION
from vonage_cloud_runtime.providers.state.enums.fullText.ISearchOptions import ISearchOptions
T = TypeVar('T')

#interface
class IState(ABC):
    @abstractmethod
    def set(self,key: str,value: T):
        pass
    @abstractmethod
    def get(self,key: str):
        pass
    @abstractmethod
    def delete(self,key: str):
        pass
    @abstractmethod
    def increment(self,key: str,value: int):
        pass
    @abstractmethod
    def decrement(self,key: str,value: int):
        pass
    @abstractmethod
    def expire(self,key: str,seconds: int,option: EXPIRE_OPTION = None):
        pass
    @abstractmethod
    def mapDelete(self,table: str,keys: List[str]):
        pass
    @abstractmethod
    def mapExists(self,table: str,key: str):
        pass
    @abstractmethod
    def mapGetAll(self,table: str):
        pass
    @abstractmethod
    def mapGetMultiple(self,table: str,keys: List[str]):
        pass
    @abstractmethod
    def mapGetValues(self,table: str):
        pass
    @abstractmethod
    def mapGetValue(self,table: str,key: str):
        pass
    @abstractmethod
    def mapIncrement(self,table: str,key: str,value: int):
        pass
    @abstractmethod
    def mapLength(self,table: str):
        pass
    @abstractmethod
    def mapSet(self,table: str,keyValuePairs: Dict[str,str]):
        pass
    @abstractmethod
    def mapScan(self,table: str,cursor: str,pattern: str = None,count: int = None):
        pass
    @abstractmethod
    def listAppend(self,list: str,value: T):
        pass
    @abstractmethod
    def listPrepend(self,list: str,value: T):
        pass
    @abstractmethod
    def listEndPop(self,list: str,count: int):
        pass
    @abstractmethod
    def listStartPop(self,list: str,count: int):
        pass
    @abstractmethod
    def listRemove(self,list: str,value: T,count: int):
        pass
    @abstractmethod
    def listTrim(self,list: str,startPos: int,endPos: int):
        pass
    @abstractmethod
    def listInsert(self,list: str,before: bool,pivot: T,value: T):
        pass
    @abstractmethod
    def listIndex(self,list: str,position: int):
        pass
    @abstractmethod
    def listSet(self,list: str,position: int,value: T):
        pass
    @abstractmethod
    def listLength(self,list: str):
        pass
    @abstractmethod
    def listRange(self,list: str,startPos: int,endPos: int):
        pass
    @abstractmethod
    def createIndex(self,name: str,options: CreateIndexOptions):
        pass
    @abstractmethod
    def search(self,index: str,query: str,options: ISearchOptions = None):
        pass
    @abstractmethod
    def dropIndex(self,index: str,deleteDocs: bool = None):
        pass
