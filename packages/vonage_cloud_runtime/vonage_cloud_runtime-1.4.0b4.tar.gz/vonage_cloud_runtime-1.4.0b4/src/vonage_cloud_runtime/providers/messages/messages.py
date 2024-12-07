from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.messages.enums.messageAction import MESSAGE_ACTION
from vonage_cloud_runtime.providers.messages.IMessages import IMessages
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.messages.contracts.IMessageContact import IMessageContact
from vonage_cloud_runtime.providers.messages.contracts.listenEventsPayload import ListenEventsPayload
from vonage_cloud_runtime.providers.messages.contracts.listenMessagesPayload import ListenMessagesPayload
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.providers.messages.contracts.IListenMessagesPayload import IListenMessagesPayload

@dataclass
class Messages(IMessages):
    session: ISession
    provider: str = field(default = "vonage-messaging")
    def __init__(self,session: ISession):
        self.session = session
    
    async def onMessage(self,callback: str,from_: IMessageContact,to: IMessageContact):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = ListenMessagesPayload(from_,to,self.session.wrapCallback(callback,[]))
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.url = self.session.config.getExecutionUrl(self.provider,MESSAGE_ACTION.SUBSCRIBE_INBOUND_MESSAGES)
        await self.session.request(requestParams)
        return requestParams.data.callback.id
    
    async def onMessageEvent(self,callback: str,from_: IMessageContact,to: IMessageContact):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = ListenEventsPayload(from_,to,self.session.wrapCallback(callback,[]))
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.url = self.session.config.getExecutionUrl(self.provider,MESSAGE_ACTION.SUBSCRIBE_INBOUND_EVENTS)
        await self.session.request(requestParams)
        return requestParams.data.callback.id
    
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
