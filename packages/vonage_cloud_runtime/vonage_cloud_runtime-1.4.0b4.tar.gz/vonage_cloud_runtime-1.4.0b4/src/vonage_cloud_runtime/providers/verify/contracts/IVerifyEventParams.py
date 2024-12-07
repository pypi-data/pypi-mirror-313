from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IVerifyEventParams(ABC):
    subscriptionName:str
    callback:str
    type_:str
    status:str
