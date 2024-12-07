from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.enums.fullText.IndexType import IndexType
from vonage_cloud_runtime.providers.state.contracts.fullText.ICreateIndexOptions import ICreateIndexOptions
from vonage_cloud_runtime.providers.state.contracts.fullText.prefixOptions import PrefixOptions
from vonage_cloud_runtime.providers.state.contracts.fullText.schemaField import SchemaField
from vonage_cloud_runtime.providers.state.contracts.fullText.stopwordsOptions import StopwordsOptions

@dataclass
class CreateIndexOptions(ICreateIndexOptions):
    prefix: PrefixOptions
    schema: List[SchemaField]
    on: IndexType = None
    filter: str = None
    language: str = None
    languageField: str = None
    score: int = None
    scoreField: str = None
    payloadField: str = None
    maxTextFields: bool = None
    temporary: int = None
    noOffsets: bool = None
    noHl: bool = None
    noFields: bool = None
    noFreqs: bool = None
    stopwords: StopwordsOptions = None
    skipInitialScan: bool = None
    def __init__(self):
        pass
    def reprJSON(self):
        result = {}
        dict = asdict(self)
        keywordsMap = {"from_":"from","del_":"del","import_":"import","type_":"type", "return_":"return"}
        for key in dict:
            val = getattr(self, key)

            if val is not None:
                if type(val) is list:
                    parsedList = []
                    for i in val:
                        if hasattr(i,'reprJSON'):
                            parsedList.append(i.reprJSON())
                        else:
                            parsedList.append(i)
                    val = parsedList

                if hasattr(val,'reprJSON'):
                    val = val.reprJSON()
                if key in keywordsMap:
                    key = keywordsMap[key]
                result.__setitem__(key.replace('_hyphen_', '-'), val)
        return result
