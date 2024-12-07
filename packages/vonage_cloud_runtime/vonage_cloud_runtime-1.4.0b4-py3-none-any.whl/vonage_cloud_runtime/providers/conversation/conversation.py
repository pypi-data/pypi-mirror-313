from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.conversation.enums.conversationAction import CONVERSATION_ACTION
from vonage_cloud_runtime.providers.conversation.IConversation import IConversation
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.session.contracts.IFilter import IFilter
from vonage_cloud_runtime.providers.conversation.contracts.conversationPayloadWithCallback import ConversationPayloadWithCallback
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.session.contracts.filter import Filter

@dataclass
class Conversation(IConversation):
    session: ISession
    provider: str = field(default = "vonage-voice")
    def __init__(self,session: ISession):
        self.session = session
    
    async def onConversationEvent(self,callback: str,events: List[str] = None):
        filters = []
        if events is not None:
            filters.append(Filter("type","contains",events))
        
        rp = RequestParams()
        rp.method = REQUEST_VERB.POST
        rp.data = ConversationPayloadWithCallback(self.session.wrapCallback(callback,filters))
        rp.url = self.session.config.getExecutionUrl(self.provider,CONVERSATION_ACTION.CONVERSATION_SUBSCRIBE_EVENT)
        rp.headers = self.session.constructRequestHeaders()
        await self.session.request(rp)
        return rp.data.callback.id
    
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
