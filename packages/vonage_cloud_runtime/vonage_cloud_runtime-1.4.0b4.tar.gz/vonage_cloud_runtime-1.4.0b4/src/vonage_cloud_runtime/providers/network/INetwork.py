from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.network.contracts.INumberVerificationEventParams import INumberVerificationEventParams


#interface
class INetwork(ABC):
    @abstractmethod
    def onNumberVerificationEvent(self,params: INumberVerificationEventParams):
        pass
    @abstractmethod
    def getNumberVerificationRedirectURI(self):
        pass
