from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.enums.fullText.FieldType import FieldType


#interface
class ISchemaField(ABC):
    fieldName:str
    alias:str
    type_:FieldType
    sortable:bool
    unf:bool
    noIndex:bool
