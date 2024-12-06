from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')
T = TypeVar("T")


#interface
class IVCREvent(ABC,Generic[T]):
    timestamp:str
    id:str
    event_type:str
    source_type:str
    source_id:str
    api_account_id:str
    api_application_id:str
    session_id:str
    instance_id:str
    details:T
