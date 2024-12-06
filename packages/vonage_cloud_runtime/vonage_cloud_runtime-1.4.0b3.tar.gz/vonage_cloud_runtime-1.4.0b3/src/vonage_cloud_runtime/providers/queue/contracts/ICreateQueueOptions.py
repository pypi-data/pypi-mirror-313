from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class ICreateQueueOptions(ABC):
    maxInflight:int
    msgPerSecond:int
    active:bool
