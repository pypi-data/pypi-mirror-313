from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.queue.contracts.IQueueDetails import IQueueDetails
from vonage_cloud_runtime.providers.queue.contracts.IQueueDetailsStats import IQueueDetailsStats


#interface
class QueueDetailsResponse(ABC):
    queueDetails:IQueueDetails
    stats:IQueueDetailsStats
