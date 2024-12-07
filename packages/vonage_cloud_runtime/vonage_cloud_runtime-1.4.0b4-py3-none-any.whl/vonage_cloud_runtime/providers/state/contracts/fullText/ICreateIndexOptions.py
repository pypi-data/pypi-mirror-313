from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.enums.fullText.IndexType import IndexType
from vonage_cloud_runtime.providers.state.contracts.fullText.prefixOptions import PrefixOptions
from vonage_cloud_runtime.providers.state.contracts.fullText.schemaField import SchemaField
from vonage_cloud_runtime.providers.state.contracts.fullText.stopwordsOptions import StopwordsOptions


#interface
class ICreateIndexOptions(ABC):
    schema:List[SchemaField]
    prefix:PrefixOptions
    on:IndexType
    filter:str
    language:str
    languageField:str
    score:int
    scoreField:str
    payloadField:str
    maxTextFields:bool
    temporary:int
    noOffsets:bool
    noHl:bool
    noFields:bool
    noFreqs:bool
    stopwords:StopwordsOptions
    skipInitialScan:bool
