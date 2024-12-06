from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.enums.fullText.ITags import ITags


#interface
class IHighlightOption(ABC):
    fields:List[str]
    tags:ITags
