from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.events.IEventFactory import IEventFactory
from vonage_cloud_runtime.providers.events.contracts.IVCREvent import IVCREvent
from vonage_cloud_runtime.providers.events.contracts.vcrEvent import VCREvent
from vonage_cloud_runtime.providers.events.enums.vcrEventSourceType import VCR_EVENT_SOURCE_TYPE
from vonage_cloud_runtime.providers.events.enums.vcrEventType import VCR_EVENT_TYPE
T = TypeVar('T')
@dataclass
class EventFactory(IEventFactory):
    bridge: IBridge
    session: ISession
    def __init__(self,session: ISession):
        self.session = session
        self.bridge = session.bridge
    
    def createEvent(self,eventName: str,details: T):
        if eventName is VCR_EVENT_TYPE.SESSION_CREATED:
            event = VCREvent()
            event.event_type = VCR_EVENT_TYPE.SESSION_CREATED
            event.source_type = VCR_EVENT_SOURCE_TYPE.INSTANCE
            event.details = details
            self.setCommonFields(event)
            return event
        
        raise self.bridge.createSdkError("Event type not supported: " + eventName)
    
    def setCommonFields(self,event: IVCREvent[T]):
        event.timestamp = self.session.bridge.isoDate()
        event.id = self.session.bridge.uuid()
        event.source_id = self.session.config.instanceServiceName
        event.api_account_id = self.session.config.apiAccountId
        event.api_application_id = self.session.config.apiApplicationId
        event.session_id = self.session.id
        event.instance_id = self.session.config.instanceId
    
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
