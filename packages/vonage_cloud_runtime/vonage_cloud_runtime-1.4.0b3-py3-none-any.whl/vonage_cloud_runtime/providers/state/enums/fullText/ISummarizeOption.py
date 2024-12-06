from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class ISummarizeOption(ABC):
    fields:List[str]
    frags:int
    len:int
    separator:str
