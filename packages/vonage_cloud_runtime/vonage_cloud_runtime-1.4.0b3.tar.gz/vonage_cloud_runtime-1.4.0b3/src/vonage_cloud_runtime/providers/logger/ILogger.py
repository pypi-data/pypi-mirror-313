from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.logger.contracts.ILogContext import ILogContext


#interface
class ILogger(ABC):
    @abstractmethod
    def log(self,level: str,message: str,context: ILogContext = None):
        pass
