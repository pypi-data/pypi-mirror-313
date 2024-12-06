from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.scheduler.contracts.IIntervalParams import IIntervalParams
from vonage_cloud_runtime.session.contracts.IPayloadWithCallback import IPayloadWithCallback
T = TypeVar('T')
T = TypeVar("T")


#interface
class IStartAtPayload(IPayloadWithCallback,Generic[T]):
    startAt:str
    interval:IIntervalParams
    payload:T
    id:str
