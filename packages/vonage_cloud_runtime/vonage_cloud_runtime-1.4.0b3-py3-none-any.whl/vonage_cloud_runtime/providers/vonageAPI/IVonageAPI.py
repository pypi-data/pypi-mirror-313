from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')
K = TypeVar('K')

#interface
class IVonageAPI(ABC):
    @abstractmethod
    def invoke(self,url: str,method: str,body: T,headers: Dict[str,str] = None):
        pass
