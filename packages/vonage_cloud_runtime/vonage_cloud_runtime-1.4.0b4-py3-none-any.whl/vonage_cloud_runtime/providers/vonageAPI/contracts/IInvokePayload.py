from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')
T = TypeVar("T")


#interface
class IInvokePayload(ABC,Generic[T]):
    url:str
    method:str
    body:T
