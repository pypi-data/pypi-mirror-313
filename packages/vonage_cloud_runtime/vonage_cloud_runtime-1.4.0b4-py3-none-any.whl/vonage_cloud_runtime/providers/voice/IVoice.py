from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.voice.contracts.ICallEventParams import ICallEventParams


#interface
class IVoice(ABC):
    @abstractmethod
    def onCall(self,callback: str):
        pass
    @abstractmethod
    def onCallEvent(self,params: ICallEventParams):
        pass
    @abstractmethod
    def getCallRecording(self,recordingUrl: str):
        pass
    @abstractmethod
    def uploadCallRecording(self,recordingUrl: str,assetsPath: str):
        pass
