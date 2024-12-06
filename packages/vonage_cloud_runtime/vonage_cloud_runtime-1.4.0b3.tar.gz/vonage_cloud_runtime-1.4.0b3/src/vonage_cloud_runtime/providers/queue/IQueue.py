from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.queue.contracts.ICreateQueueOptions import ICreateQueueOptions
from vonage_cloud_runtime.providers.queue.contracts.queueDetailsResponse import QueueDetailsResponse
from vonage_cloud_runtime.providers.queue.contracts.IUpdateQueueOptions import IUpdateQueueOptions
T = TypeVar('T')

#interface
class IQueue(ABC):
    @abstractmethod
    def createQueue(self,queueName: str,callback: str,options: ICreateQueueOptions):
        pass
    @abstractmethod
    def updateQueue(self,queueName: str,options: IUpdateQueueOptions):
        pass
    @abstractmethod
    def list(self):
        pass
    @abstractmethod
    def getQueueDetails(self,name: str):
        pass
    @abstractmethod
    def deleteQueue(self,name: str):
        pass
    @abstractmethod
    def pauseQueue(self,name: str):
        pass
    @abstractmethod
    def resumeQueue(self,name: str):
        pass
    @abstractmethod
    def enqueue(self,name: str,data: List[T]):
        pass
    @abstractmethod
    def enqueueSingle(self,name: str,data: T):
        pass
    @abstractmethod
    def deadLetterList(self,name: str):
        pass
    @abstractmethod
    def deadLetterDequeue(self,name: str,count: int):
        pass
