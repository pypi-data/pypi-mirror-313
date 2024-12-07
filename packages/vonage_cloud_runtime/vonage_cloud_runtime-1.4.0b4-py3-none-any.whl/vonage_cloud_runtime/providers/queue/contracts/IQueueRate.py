from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IQueueRate(ABC):
    msgPerSecond:int
    maxInflight:int
