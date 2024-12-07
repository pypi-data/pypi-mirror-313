from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.providers.vonageAPI.vonageAPIActions import VonageAPIActions
from vonage_cloud_runtime.providers.vonageAPI.IVonageAPI import IVonageAPI
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.vonageAPI.contracts.invokePayload import InvokePayload
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
T = TypeVar('T')
K = TypeVar('K')
@dataclass
class VonageAPI(IVonageAPI):
    bridge: IBridge
    session: ISession
    provider: str = field(default = "vonage-api")
    def __init__(self,session: ISession):
        self.session = session
        self.bridge = session.bridge
    
    async def invoke(self,url: str,method: str,body: T,headers: Dict[str,str] = None):
        payload = InvokePayload(url,method,body)
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = payload
        requestParams.headers = self.session.constructRequestHeaders()
        if headers is not None:
            keys = self.bridge.getObjectKeys(headers)
            for i in range(0,keys.__len__()):
                requestParams.headers[keys[i]] = headers[keys[i]]
            
        
        requestParams.url = self.session.config.getExecutionUrl(self.provider,VonageAPIActions.INVOKE)
        return await self.session.request(requestParams)
    
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
