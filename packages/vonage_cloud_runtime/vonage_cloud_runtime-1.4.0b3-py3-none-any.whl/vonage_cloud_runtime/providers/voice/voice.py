from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.voice.enums.voiceAction import VOICE_ACTION
from vonage_cloud_runtime.providers.voice.IVoice import IVoice
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.voice.contracts.ICallEventParams import ICallEventParams
from vonage_cloud_runtime.providers.voice.contracts.callAnswerCallBack import CallAnswerCallBack
from vonage_cloud_runtime.providers.voice.contracts.CallEventCallBackPayload import CallEventCallBackPayload
from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.request.enums.responseTypes import RESPONSE_TYPE
from vonage_cloud_runtime.services.jwt.contracts.createVonageTokenParams import CreateVonageTokenParams
from vonage_cloud_runtime.providers.assets.assets import Assets
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB

@dataclass
class Voice(IVoice):
    bridge: IBridge
    assetsAPI: Assets
    session: ISession
    provider: str = field(default = "vonage-voice")
    def __init__(self,session: ISession):
        self.session = session
        self.bridge = session.bridge
        self.assetsAPI = Assets(session)
    
    async def onCall(self,callback: str):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = CallAnswerCallBack(self.session.wrapCallback(callback,[]))
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.url = self.session.config.getExecutionUrl(self.provider,VOICE_ACTION.VAPI_SUBSCRIBE_INBOUND_CALL)
        await self.session.request(requestParams)
        return requestParams.data.callback.id
    
    async def onCallEvent(self,params: ICallEventParams):
        payload = CallEventCallBackPayload()
        payload.callback = self.session.wrapCallback(params.callback,[])
        if params.vapiID is not None:
            payload.vapiId = params.vapiID
        
        elif params.conversationID is not None:
            payload.conversationId = params.conversationID
        
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = payload
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.url = self.session.config.getExecutionUrl(self.provider,VOICE_ACTION.VAPI_SUBSCRIBE_EVENT)
        await self.session.request(requestParams)
        return payload.callback.id
    
    async def getCallRecording(self,recordingUrl: str):
        tp = CreateVonageTokenParams()
        tp.exp = self.bridge.getSystemTime() + 60 * 60
        t = self.session.jwt.createVonageToken(tp)
        rp = RequestParams()
        rp.method = REQUEST_VERB.GET
        rp.url = recordingUrl
        rp.headers = {}
        rp.headers.Authorization = f'Bearer {t}'
        rp.responseType = RESPONSE_TYPE.STREAM
        return await self.session.request(rp)
    
    async def uploadCallRecording(self,recordingUrl: str,assetsPath: str):
        stream = await self.getCallRecording(recordingUrl)
        pathObject = self.bridge.parsePath(assetsPath)
        data = [stream]
        fileNames = [pathObject.base]
        return await self.assetsAPI.uploadData(data,pathObject.dir,fileNames)
    
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
