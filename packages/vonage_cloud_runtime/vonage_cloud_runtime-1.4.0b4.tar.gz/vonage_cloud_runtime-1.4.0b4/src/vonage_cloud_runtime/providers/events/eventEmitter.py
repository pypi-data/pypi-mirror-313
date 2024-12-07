from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.services.config.IConfig import IConfig
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.events.eventFactory import EventFactory
from vonage_cloud_runtime.providers.events.IEventEmitter import IEventEmitter
from vonage_cloud_runtime.providers.events.IEventFactory import IEventFactory
from vonage_cloud_runtime.providers.events.contracts.ISessionCreatedDetails import ISessionCreatedDetails
from vonage_cloud_runtime.providers.events.contracts.sessionCreatedDetails import SessionCreatedDetails
from vonage_cloud_runtime.providers.events.enums.vcrEventType import VCR_EVENT_TYPE
from vonage_cloud_runtime.providers.events.contracts.IVCREvent import IVCREvent
T = TypeVar('T')
@dataclass
class EventEmitter(IEventEmitter):
    url: str
    session: ISession
    eventFactory: IEventFactory
    bridge: IBridge
    config: IConfig
    provider: str = field(default = "events-submission")
    def __init__(self,session: ISession):
        self.config = session.config
        self.bridge = session.bridge
        self.session = session
        self.eventFactory = EventFactory(self.session)
        self.url = self.config.getExecutionUrl(self.provider)
    
    async def emitSessionCreatedEvent(self,ttl: int):
        expiresAt = self.bridge.toISOString(ttl)
        details = SessionCreatedDetails(expiresAt)
        event = self.eventFactory.createEvent(VCR_EVENT_TYPE.SESSION_CREATED,details)
        await self.emit(event)
    
    async def emit(self,e: T):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.url = self.url
        requestParams.data = e
        requestParams.headers = self.session.constructRequestHeaders()
        await self.bridge.requestWithoutResponse(requestParams)
    
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
