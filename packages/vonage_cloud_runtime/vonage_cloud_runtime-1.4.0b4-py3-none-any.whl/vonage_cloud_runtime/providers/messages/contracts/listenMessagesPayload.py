from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.messages.contracts.IListenMessagesPayload import IListenMessagesPayload
from vonage_cloud_runtime.providers.messages.contracts.IMessageContact import IMessageContact
from vonage_cloud_runtime.session.contracts.IWrappedCallback import IWrappedCallback

@dataclass
class ListenMessagesPayload(IListenMessagesPayload):
    callback: IWrappedCallback
    to: IMessageContact
    from_: IMessageContact
    def __init__(self,from_: IMessageContact,to: IMessageContact,callback: IWrappedCallback):
        self.from_ = from_
        self.to = to
        self.callback = callback
    
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
