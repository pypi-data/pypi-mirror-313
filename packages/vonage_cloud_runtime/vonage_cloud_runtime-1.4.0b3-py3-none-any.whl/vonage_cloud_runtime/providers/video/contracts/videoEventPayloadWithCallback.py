from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.session.contracts.IWrappedCallback import IWrappedCallback
from vonage_cloud_runtime.providers.video.contracts.IVideoEventCallback import IVideoEventCallback

@dataclass
class VideoEventPayloadWithCallback(IVideoEventCallback):
    provider: str
    matchFields: Dict[str,str]
    event: str
    callback: IWrappedCallback
    name: str
    def __init__(self,name: str,event: str,callback: IWrappedCallback,matchFields: Dict[str,str]):
        self.name = name
        self.callback = callback
        self.event = event
        self.matchFields = matchFields
        self.provider = "vonage"
    
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
