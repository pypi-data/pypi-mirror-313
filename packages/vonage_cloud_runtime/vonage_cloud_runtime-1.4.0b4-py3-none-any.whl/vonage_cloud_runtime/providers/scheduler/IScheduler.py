from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.scheduler.contracts.IStartAtParams import IStartAtParams
from vonage_cloud_runtime.providers.scheduler.contracts.listAllSchedulersResponse import ListAllSchedulersResponse
from vonage_cloud_runtime.providers.scheduler.contracts.getSchedulerResponse import GetSchedulerResponse
T = TypeVar('T')

#interface
class IScheduler(ABC):
    @abstractmethod
    def startAt(self,params: IStartAtParams[T]):
        pass
    @abstractmethod
    def list(self,size: int = None,cursor: str = None):
        pass
    @abstractmethod
    def get(self,scheduleId: str):
        pass
    @abstractmethod
    def cancel(self,scheduleId: str):
        pass
