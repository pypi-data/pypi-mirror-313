from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IPathObject(ABC):
    dir:str
    base:str
    ext:str
    name:str
    root:str
