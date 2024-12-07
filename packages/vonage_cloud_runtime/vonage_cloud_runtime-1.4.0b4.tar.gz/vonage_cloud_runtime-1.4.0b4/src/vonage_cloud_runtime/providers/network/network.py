from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.network.INetwork import INetwork
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.network.contracts.numberVerificationEventCallback import NumberVerificationEventCallback
from vonage_cloud_runtime.providers.network.contracts.INumberVerificationEventParams import INumberVerificationEventParams
from vonage_cloud_runtime.IBridge import IBridge

@dataclass
class Network(INetwork):
    bridge: IBridge
    session: ISession
    def __init__(self,session: ISession):
        self.session = session
        self.bridge = self.session.bridge
    
    async def onNumberVerificationEvent(self,params: INumberVerificationEventParams):
        rp = RequestParams()
        rp.method = REQUEST_VERB.POST
        rp.data = NumberVerificationEventCallback(params.subscriptionName,self.session.wrapCallback(params.callback,[]),{})
        rp.url = self.session.config.getSubscriptionUrl()
        rp.headers = self.session.constructRequestHeaders()
        await self.session.request(rp)
        return rp.data.callback.id
    
    def getNumberVerificationRedirectURI(self):
        config = self.session.config
        appID = config.apiApplicationId
        accountID = config.apiAccountId
        regionPrefix = "aws."
        if self.bridge.testRegEx(config.region,f'^{regionPrefix}*') is not True:
            raise self.bridge.createSdkError(f'could not construct redirect url, region has wrong format')
        
        region = self.bridge.substring(config.region,regionPrefix.__len__(),config.region.__len__())
        return f'https://universal-callback-service.{region}.runtime.vonage.cloud/onEvent?provider=vonage&event=network.nv&apiApplicationId={appID}&apiAccountId={accountID}'
    
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
