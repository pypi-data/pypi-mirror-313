from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge


#interface
class IConfig(ABC):
    bridge:IBridge
    instanceServiceName:str
    applicationId:str
    apiApplicationId:str
    apiAccountId:str
    apiAccountSecret:str
    instanceId:str
    privateKey:str
    debug:bool
    region:str
    appUrl:str
    assetUrl:str
    namespace:str
    logsSubmission:bool
    @abstractmethod
    def getSubscriptionUrl(self):
        pass
    @abstractmethod
    def getExecutionUrl(self,func: str,pathname: str = None,queryParams: Dict[str,str] = None):
        pass
