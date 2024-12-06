from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.enums.fullText.unit import Unit


#interface
class IGeoFilterOption(ABC):
    geoField:str
    lon:int
    lat:int
    radius:int
    unit:Unit
