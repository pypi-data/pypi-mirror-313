from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.session.vcrSession import VCRSession
from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.services.config.IConfig import IConfig
from vonage_cloud_runtime.services.jwt.jwt import JWT
from vonage_cloud_runtime.bridge import Bridge
from vonage_cloud_runtime.services.config.config import Config
from vonage_cloud_runtime.request.contracts.IRequest import IRequest
from vonage_cloud_runtime.providers.state.state import State
from vonage_cloud_runtime.services.jwt.IJwt import IJWT
from vonage_cloud_runtime.IVCR import IVCR
from vonage_cloud_runtime.services.jwt.contracts.ICreateVonageTokenParams import ICreateVonageTokenParams
from vonage_cloud_runtime.providers.messages.contracts.unsubscribeEventsPayload import UnsubscribeEventsPayload
from vonage_cloud_runtime.session.contracts.actionPayload import ActionPayload
from vonage_cloud_runtime.providers.messages.enums.messageAction import MESSAGE_ACTION
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.session.contracts.command import Command
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB

@dataclass
class VCR(IVCR):
    jwt: IJWT
    config: IConfig
    bridge: IBridge
    def __init__(self):
        self.bridge = Bridge()
        self.config = Config(self.bridge)
        self.jwt = JWT(self.bridge,self.config)
    
    async def unsubscribe(self,id: str,provider: str = "vonage-messaging"):
        p = UnsubscribeEventsPayload(id)
        a = ActionPayload(provider,MESSAGE_ACTION.UNSUBSCRIBE_EVENTS,p)
        s = self.getGlobalSession()
        ch = s.constructCommandHeaders()
        rp = RequestParams()
        rp.method = REQUEST_VERB.POST
        rp.data = Command(ch,a)
        rp.headers = s.constructRequestHeaders()
        rp.url = s.config.getExecutionUrl(provider)
        return await s.request(rp)
    
    def createVonageToken(self,params: ICreateVonageTokenParams):
        if params is None:
            raise self.bridge.createSdkError("createVonageToken: params is required")
        
        if params.exp is None:
            raise self.bridge.createSdkError("createVonageToken: params.exp is required")
        
        return self.jwt.createVonageToken(params)
    
    def createSession(self,ttl: int = 7 * 24 * 60 * 60):
        if self.bridge.isInteger(ttl) is False or ttl < 0:
            raise self.bridge.createSdkError("createSession: ttl must be a positive integer")
        
        id = self.bridge.uuid()
        session = self.createSessionWithId(id)
        self.bridge.runBackgroundTask(session.emitSessionCreatedEvent(ttl))
        return session
    
    def createSessionWithId(self,id: str):
        return VCRSession(self.bridge,self.config,self.jwt,id)
    
    def getSessionById(self,id: str):
        if id is None:
            raise self.bridge.createSdkError("getSessionById: id is required")
        
        return self.createSessionWithId(id)
    
    def getAppUrl(self):
        return self.config.appUrl
    
    def getSessionFromRequest(self,req: IRequest):
        if req is None:
            raise self.bridge.createSdkError("getSessionFromRequest: function requires request object to be provided")
        
        if req.headers is None:
            raise self.bridge.createSdkError("getSessionFromRequest: invalid request object proivided")
        
        id = req.headers["x-neru-sessionid"]
        if id is None:
            raise self.bridge.createSdkError(f'getSessionFromRequest: request does not contain \"x-neru-sessionid\" header')
        
        return self.getSessionById(id)
    
    def getGlobalSession(self):
        uuid = "00000000-0000-0000-0000-000000000000"
        return self.getSessionById(uuid)
    
    def getInstanceState(self):
        session = self.getGlobalSession()
        return State(session,f'application:{self.config.instanceId}')
    
    def getAccountState(self):
        session = self.getGlobalSession()
        return State(session,"account")
    
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
