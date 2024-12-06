from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.session.contracts.IWrappedCallback import IWrappedCallback
from vonage_cloud_runtime.providers.queue.contracts.IQueueRate import IQueueRate


#interface
class IQueueDetails(ABC):
    name:str
    callback:IWrappedCallback
    rate:IQueueRate
    active:bool
