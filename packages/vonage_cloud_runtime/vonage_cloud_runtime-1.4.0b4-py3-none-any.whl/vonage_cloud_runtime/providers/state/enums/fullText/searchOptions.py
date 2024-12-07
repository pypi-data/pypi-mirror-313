from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.enums.fullText.ISearchOptions import ISearchOptions
from vonage_cloud_runtime.providers.state.enums.fullText.filterOption import FilterOption
from vonage_cloud_runtime.providers.state.enums.fullText.geoFilterOption import GeoFilterOption
from vonage_cloud_runtime.providers.state.enums.fullText.highlightOption import HighlightOption
from vonage_cloud_runtime.providers.state.enums.fullText.inFieldsOption import InFieldsOption
from vonage_cloud_runtime.providers.state.enums.fullText.inKeysOptions import InKeysOption
from vonage_cloud_runtime.providers.state.enums.fullText.limitOption import LimitOption
from vonage_cloud_runtime.providers.state.enums.fullText.paramOption import ParamOption
from vonage_cloud_runtime.providers.state.enums.fullText.returnOption import ReturnOption
from vonage_cloud_runtime.providers.state.enums.fullText.sortByOption import SortByOption
from vonage_cloud_runtime.providers.state.enums.fullText.summarizeOption import SummarizeOption

@dataclass
class SearchOptions(ISearchOptions):
    noContent: bool = None
    verbatim: bool = None
    noStopwords: bool = None
    withScores: bool = None
    withPayloads: bool = None
    withSortKeys: bool = None
    filters: List[FilterOption] = None
    geoFilters: List[GeoFilterOption] = None
    inKeys: InKeysOption = None
    inFields: InFieldsOption = None
    return_: ReturnOption = None
    summarize: SummarizeOption = None
    highlight: HighlightOption = None
    slop: int = None
    timeout: int = None
    inorder: bool = None
    language: str = None
    expander: str = None
    scorer: str = None
    explainScore: bool = None
    payload: str = None
    sortBy: SortByOption = None
    limit: LimitOption = None
    params: List[ParamOption] = None
    dialect: str = None
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
