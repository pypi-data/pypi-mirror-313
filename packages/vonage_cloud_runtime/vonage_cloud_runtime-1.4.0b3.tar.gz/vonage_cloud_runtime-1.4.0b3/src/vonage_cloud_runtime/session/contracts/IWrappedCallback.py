from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.session.contracts.IFilter import IFilter


#interface
class IWrappedCallback(ABC):
    id:str
    filters:List[IFilter]
    instanceServiceName:str
    sessionId:str
    instanceId:str
    path:str
