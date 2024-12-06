from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.video.IVideo import IVideo
from vonage_cloud_runtime.providers.video.contracts.IVideoEventParams import IVideoEventParams
from vonage_cloud_runtime.providers.video.contracts.IVideoSessionEventParams import IVideoSessionEventParams
from vonage_cloud_runtime.providers.video.contracts.videoEventPayloadWithCallback import VideoEventPayloadWithCallback

@dataclass
class Video(IVideo):
    session: ISession
    def __init__(self,session: ISession):
        self.session = session
    
    async def onSessionEvent(self,params: IVideoSessionEventParams):
        rp = RequestParams()
        matchedFields = {}
        if params.sessionId is not None:
            matchedFields["sessionId"] = params.sessionId
        
        if params.connectionId is not None:
            matchedFields["connectionId"] = params.connectionId
        
        if params.streamId is not None:
            matchedFields["streamId"] = params.streamId
        
        rp.method = REQUEST_VERB.POST
        rp.data = VideoEventPayloadWithCallback(params.subscriptionName,"video.session",self.session.wrapCallback(params.callback,[]),matchedFields)
        rp.url = self.session.config.getSubscriptionUrl()
        rp.headers = self.session.constructRequestHeaders()
        await self.session.request(rp)
        return rp.data.callback.id
    
    async def onRecordingEvent(self,params: IVideoEventParams):
        rp = self.buildVideoEventReq(params,"video.recording")
        await self.session.request(rp)
        return rp.data.callback.id
    
    async def onBroadcastEvent(self,params: IVideoEventParams):
        rp = self.buildVideoEventReq(params,"video.streaming")
        await self.session.request(rp)
        return rp.data.callback.id
    
    async def onComposerEvent(self,params: IVideoEventParams):
        rp = self.buildVideoEventReq(params,"video.composer")
        await self.session.request(rp)
        return rp.data.callback.id
    
    async def onCaptionEvent(self,params: IVideoEventParams):
        rp = self.buildVideoEventReq(params,"video.caption")
        await self.session.request(rp)
        return rp.data.callback.id
    
    async def onSipEvent(self,params: IVideoEventParams):
        rp = self.buildVideoEventReq(params,"video.sip")
        await self.session.request(rp)
        return rp.data.callback.id
    
    def buildVideoEventReq(self,params: IVideoEventParams,event: str):
        rp = RequestParams()
        matchedFields = {}
        if params.sessionId is not None:
            matchedFields["sessionId"] = params.sessionId
        
        rp.method = REQUEST_VERB.POST
        rp.data = VideoEventPayloadWithCallback(params.subscriptionName,event,self.session.wrapCallback(params.callback,[]),matchedFields)
        rp.url = self.session.config.getSubscriptionUrl()
        rp.headers = self.session.constructRequestHeaders()
        return rp
    
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
