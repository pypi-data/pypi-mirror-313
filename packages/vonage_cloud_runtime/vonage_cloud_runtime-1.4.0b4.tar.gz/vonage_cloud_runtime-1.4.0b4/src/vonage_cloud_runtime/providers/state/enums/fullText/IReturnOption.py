from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.enums.fullText.fieldProperty import FieldProperty


#interface
class IReturnOption(ABC):
    count:int
    fields:List[FieldProperty]
