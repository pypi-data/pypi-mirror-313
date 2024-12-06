from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.request.enums.dataType import DATA_TYPE
from vonage_cloud_runtime.request.enums.responseTypes import RESPONSE_TYPE
T = TypeVar('T')
T = TypeVar("T")


#interface
class IRequestParams(ABC,Generic[T]):
    method:str
    url:str
    data:T
    headers:Dict[str,str]
    responseType:RESPONSE_TYPE
    dataType:DATA_TYPE
