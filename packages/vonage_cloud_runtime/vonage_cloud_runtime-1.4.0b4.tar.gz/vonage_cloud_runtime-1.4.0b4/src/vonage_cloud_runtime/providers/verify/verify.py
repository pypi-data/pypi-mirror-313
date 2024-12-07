from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.verify.IVerify import IVerify
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.verify.contracts.verifyStatusPayloadWithCallback import VerifyStatusPayloadWithCallback
from vonage_cloud_runtime.providers.verify.contracts.IVerifyEventParams import IVerifyEventParams

@dataclass
class Verify(IVerify):
    session: ISession
    def __init__(self,session: ISession):
        self.session = session
    
    async def onVerifyEvent(self,params: IVerifyEventParams):
        rp = RequestParams()
        matchedFields = {}
        if params.status is not None:
            matchedFields["status"] = params.status
        
        if params.type_:
            matchedFields["type_"] = params.type_
        
        rp.method = REQUEST_VERB.POST
        rp.data = VerifyStatusPayloadWithCallback(params.subscriptionName,self.session.wrapCallback(params.callback,[]),matchedFields)
        rp.url = self.session.config.getSubscriptionUrl()
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
