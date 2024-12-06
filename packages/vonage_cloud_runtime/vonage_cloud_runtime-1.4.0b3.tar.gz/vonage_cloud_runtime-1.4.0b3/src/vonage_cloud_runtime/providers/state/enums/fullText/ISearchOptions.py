from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.state.enums.fullText.IFilterOption import IFilterOption
from vonage_cloud_runtime.providers.state.enums.fullText.IGeoFilterOption import IGeoFilterOption
from vonage_cloud_runtime.providers.state.enums.fullText.IHighlightOption import IHighlightOption
from vonage_cloud_runtime.providers.state.enums.fullText.IInFieldsOption import IInFieldsOption
from vonage_cloud_runtime.providers.state.enums.fullText.IInKeysOption import IInKeysOption
from vonage_cloud_runtime.providers.state.enums.fullText.ILimitOption import ILimitOption
from vonage_cloud_runtime.providers.state.enums.fullText.IParamOption import IParamOption
from vonage_cloud_runtime.providers.state.enums.fullText.IReturnOption import IReturnOption
from vonage_cloud_runtime.providers.state.enums.fullText.ISortByOption import ISortByOption
from vonage_cloud_runtime.providers.state.enums.fullText.ISummarizeOption import ISummarizeOption


#interface
class ISearchOptions(ABC):
    noContent:bool
    verbatim:bool
    noStopwords:bool
    withScores:bool
    withPayloads:bool
    withSortKeys:bool
    filters:List[IFilterOption]
    geoFilters:List[IGeoFilterOption]
    inKeys:IInKeysOption
    inFields:IInFieldsOption
    return_:IReturnOption
    summarize:ISummarizeOption
    highlight:IHighlightOption
    slop:int
    timeout:int
    inorder:bool
    language:str
    expander:str
    scorer:str
    explainScore:bool
    payload:str
    sortBy:ISortByOption
    limit:ILimitOption
    params:List[IParamOption]
    dialect:str
