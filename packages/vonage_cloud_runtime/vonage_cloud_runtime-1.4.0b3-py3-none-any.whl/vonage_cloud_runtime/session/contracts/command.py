from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.session.contracts.IActionPayload import IActionPayload
from vonage_cloud_runtime.session.contracts.ICommand import ICommand
T = TypeVar('T')
T = TypeVar("T")

@dataclass
class Command(ICommand,Generic[T]):
    actions: List[IActionPayload[T]]
    header: Dict[str,str]
    def __init__(self,headers: Dict[str,str],action: IActionPayload[T]):
        self.header = headers
        self.actions = [action]
    
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
