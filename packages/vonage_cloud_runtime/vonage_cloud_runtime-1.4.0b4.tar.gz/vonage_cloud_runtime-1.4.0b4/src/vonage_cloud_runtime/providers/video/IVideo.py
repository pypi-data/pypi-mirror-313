from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.video.contracts.IVideoEventParams import IVideoEventParams
from vonage_cloud_runtime.providers.video.contracts.IVideoSessionEventParams import IVideoSessionEventParams


#interface
class IVideo(ABC):
    @abstractmethod
    def onSessionEvent(self,params: IVideoSessionEventParams):
        pass
    @abstractmethod
    def onRecordingEvent(self,params: IVideoEventParams):
        pass
    @abstractmethod
    def onBroadcastEvent(self,params: IVideoEventParams):
        pass
    @abstractmethod
    def onComposerEvent(self,params: IVideoEventParams):
        pass
    @abstractmethod
    def onCaptionEvent(self,params: IVideoEventParams):
        pass
    @abstractmethod
    def onSipEvent(self,params: IVideoEventParams):
        pass
