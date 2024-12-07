from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.verify.contracts.IVerifyEventParams import IVerifyEventParams


#interface
class IVerify(ABC):
    @abstractmethod
    def onVerifyEvent(self,params: IVerifyEventParams):
        pass
