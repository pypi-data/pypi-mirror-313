from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.providers.logger.contracts.ILogContext import ILogContext
from vonage_cloud_runtime.services.config.IConfig import IConfig
from vonage_cloud_runtime.session.contracts.IFilter import IFilter
from vonage_cloud_runtime.session.contracts.wrappedCallback import WrappedCallback
from vonage_cloud_runtime.request.contracts.IRequestParams import IRequestParams
from vonage_cloud_runtime.services.jwt.IJwt import IJWT
T = TypeVar('T')
K = TypeVar('K')

#interface
class ISession(ABC):
    jwt:IJWT
    bridge:IBridge
    config:IConfig
    id:str
    @abstractmethod
    def createUUID(self):
        pass
    @abstractmethod
    def getToken(self):
        pass
    @abstractmethod
    def log(self,level: str,message: str,context: ILogContext):
        pass
    @abstractmethod
    def wrapCallback(self,route: str,filters: List[IFilter]):
        pass
    @abstractmethod
    def constructCommandHeaders(self):
        pass
    @abstractmethod
    def constructRequestHeaders(self,useBasicAuth: bool = None):
        pass
    @abstractmethod
    def request(self,params: IRequestParams[T]):
        pass
