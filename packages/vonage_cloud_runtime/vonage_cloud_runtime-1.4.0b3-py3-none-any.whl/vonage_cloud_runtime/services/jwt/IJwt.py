from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.services.jwt.contracts.ICreateVonageTokenParams import ICreateVonageTokenParams


#interface
class IJWT(ABC):
    @abstractmethod
    def getToken(self):
        pass
    @abstractmethod
    def isExpired(self):
        pass
    @abstractmethod
    def createVonageToken(self,params: ICreateVonageTokenParams):
        pass
