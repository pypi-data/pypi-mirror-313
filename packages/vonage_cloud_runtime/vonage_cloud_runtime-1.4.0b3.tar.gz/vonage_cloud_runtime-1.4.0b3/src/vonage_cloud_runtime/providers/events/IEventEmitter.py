from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')

#interface
class IEventEmitter(ABC):
    @abstractmethod
    def emitSessionCreatedEvent(self,ttl: int):
        pass
    @abstractmethod
    def emit(self,e: T):
        pass
