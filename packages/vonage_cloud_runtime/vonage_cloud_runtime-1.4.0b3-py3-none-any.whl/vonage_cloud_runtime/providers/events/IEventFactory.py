from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.events.contracts.IVCREvent import IVCREvent
T = TypeVar('T')

#interface
class IEventFactory(ABC):
    @abstractmethod
    def createEvent(self,eventName: str,details: T):
        pass
