from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.messages.contracts.IMessageContact import IMessageContact


#interface
class IMessages(ABC):
    @abstractmethod
    def onMessage(self,callback: str,from_: IMessageContact,to: IMessageContact):
        pass
    @abstractmethod
    def onMessageEvent(self,callback: str,from_: IMessageContact,to: IMessageContact):
        pass
