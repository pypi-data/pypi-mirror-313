from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.session.contracts.IActionPayload import IActionPayload
T = TypeVar('T')
T = TypeVar("T")


#interface
class ICommand(ABC,Generic[T]):
    header:Dict[str,str]
    actions:List[IActionPayload[T]]
