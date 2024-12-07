from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IListAllPayload(ABC):
    page_size:int
    cursor:str
