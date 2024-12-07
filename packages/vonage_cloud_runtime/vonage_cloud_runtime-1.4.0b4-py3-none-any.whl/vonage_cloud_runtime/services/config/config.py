from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.services.config.IConfig import IConfig
from vonage_cloud_runtime.IBridge import IBridge

@dataclass
class Config(IConfig):
    assetUrl: str
    appUrl: str
    region: str
    privateKey: str
    apiAccountSecret: str
    apiAccountId: str
    apiApplicationId: str
    applicationId: str
    instanceServiceName: str
    bridge: IBridge
    instanceId: str = field(default = "debug")
    debug: bool = field(default = False)
    logsSubmission: bool = field(default = True)
    namespace: str = field(default = "neru")
    def __init__(self,bridge: IBridge):
        self.bridge = bridge
        if self.bridge.getEnv("NAMESPACE") is not None:
            self.namespace = self.bridge.getEnv("NAMESPACE")
        
        self.instanceServiceName = self.bridge.getEnv("INSTANCE_SERVICE_NAME")
        self.applicationId = self.bridge.getEnv("APPLICATION_ID")
        if self.bridge.getEnv("INSTANCE_ID") is not None:
            self.instanceId = self.bridge.getEnv("INSTANCE_ID")
        
        self.apiApplicationId = self.bridge.getEnv("API_APPLICATION_ID")
        self.apiAccountId = self.bridge.getEnv("API_ACCOUNT_ID")
        self.apiAccountSecret = self.bridge.getEnv("API_ACCOUNT_SECRET")
        self.privateKey = self.bridge.getEnv("PRIVATE_KEY")
        self.appUrl = self.bridge.getEnv("VCR_INSTANCE_PUBLIC_URL")
        debug = self.bridge.getEnv("DEBUG")
        if debug == "true":
            self.debug = True
        
        self.region = self.bridge.getEnv("VCR_REGION")
        self.assetUrl = "http://openfaas.euw1.dev.nexmo.cloud/function/vonage-assets?get="
    
    def getSubscriptionUrl(self):
        hostname = f'universal-callback-service.{self.namespace}'
        if self.debug:
            return self.constructDebugUrl(hostname,"subscription")
        
        return self.constructProdUrl(hostname,"subscription")
    
    def getExecutionUrl(self,func: str,pathname: str = None,queryParams: Dict[str,str] = None):
        hostname = f'{func}.{self.namespace}'
        if self.debug:
            return self.constructDebugUrl(hostname,pathname,queryParams)
        
        return self.constructProdUrl(hostname,pathname,queryParams)
    
    def constructDebugUrl(self,hostname: str,pathname: str,queryParams: Dict[str,str] = None):
        url = "http://localhost:3001"
        if pathname is not None:
            url += f'/{pathname}'
        
        url += f'?func={hostname}&async=false'
        if queryParams is not None:
            url += "&"
            url += self.queryObjectToString(queryParams)
        
        return url
    
    def constructProdUrl(self,hostname: str,pathname: str,queryParams: Dict[str,str] = None):
        url = f'http://{hostname}'
        if pathname is not None:
            url += f'/{pathname}'
        
        if queryParams is not None:
            url += "?"
            url += self.queryObjectToString(queryParams)
        
        return url
    
    def queryObjectToString(self,queryObject: Dict[str,str]):
        keys = self.bridge.getObjectKeys(queryObject)
        queryString = ""
        for i in range(0,keys.__len__()):
            key = keys[i]
            if queryObject[key] is not None:
                encodedKey = self.bridge.encodeUriComponent(key)
                value = self.bridge.encodeUriComponent(queryObject[key])
                queryString += f'{encodedKey}={value}'
                if i < keys.__len__() - 1:
                    queryString += "&"
                
            
        
        return queryString
    
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
