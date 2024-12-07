from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.state import State
from vonage_cloud_runtime.request.contracts.IRequest import IRequest
from vonage_cloud_runtime.session.vcrSession import VCRSession
from vonage_cloud_runtime.services.jwt.contracts.ICreateVonageTokenParams import ICreateVonageTokenParams


#interface
class IVCR(ABC):
    @abstractmethod
    def createVonageToken(self,params: ICreateVonageTokenParams):
        pass
    @abstractmethod
    def createSession(self,ttl: int = None):
        pass
    @abstractmethod
    def createSessionWithId(self,id: str):
        pass
    @abstractmethod
    def getSessionById(self,id: str):
        pass
    @abstractmethod
    def getAppUrl(self):
        pass
    @abstractmethod
    def getSessionFromRequest(self,req: IRequest):
        pass
    @abstractmethod
    def getGlobalSession(self):
        pass
    @abstractmethod
    def getInstanceState(self):
        pass
    @abstractmethod
    def getAccountState(self):
        pass
    @abstractmethod
    def unsubscribe(self,id: str,provider: str):
        pass
