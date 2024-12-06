from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.providers.events.eventEmitter import EventEmitter
from vonage_cloud_runtime.providers.events.IEventEmitter import IEventEmitter
from vonage_cloud_runtime.providers.logger.contracts.ILogContext import ILogContext
from vonage_cloud_runtime.providers.logger.ILogger import ILogger
from vonage_cloud_runtime.providers.logger.contracts.logContext import LogContext
from vonage_cloud_runtime.providers.logger.logger import Logger
from vonage_cloud_runtime.providers.logger.enums.logLevel import LOG_LEVEL
from vonage_cloud_runtime.services.config.IConfig import IConfig
from vonage_cloud_runtime.services.jwt.IJwt import IJWT
from vonage_cloud_runtime.session.contracts.IFilter import IFilter
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.session.contracts.wrappedCallback import WrappedCallback
from vonage_cloud_runtime.request.contracts.IRequestParams import IRequestParams
from vonage_cloud_runtime.request.enums.responseTypes import RESPONSE_TYPE
from vonage_cloud_runtime.request.enums.dataType import DATA_TYPE
T = TypeVar('T')
K = TypeVar('K')
@dataclass
class VCRSession(ISession):
    eventEmitter: IEventEmitter
    logger: ILogger
    bridge: IBridge
    jwt: IJWT
    config: IConfig
    id: str
    def __init__(self,bridge: IBridge,config: IConfig,jwt: IJWT,id: str):
        self.bridge = bridge
        self.config = config
        self.jwt = jwt
        self.id = id
        self.eventEmitter = EventEmitter(self)
        self.logger = Logger(self)
    
    async def emitSessionCreatedEvent(self,ttl: int):
        await self.eventEmitter.emitSessionCreatedEvent(ttl)
    
    def createUUID(self):
        return self.bridge.uuid()
    
    def getToken(self):
        return self.jwt.getToken()
    
    def log(self,level: str,message: str,context: ILogContext = None):
        if self.config.logsSubmission is False:
            self.bridge.log("Skipping sending logs as config.logsSubmission is set to false")
        
        elif self.bridge.getEnv("SKIP_LOGS_SUBMISSION") == "true":
            self.bridge.log("Skipping sending logs as SKIP_LOGS_SUBMISSION is set to true")
        
        else: 
            self.bridge.runBackgroundTask(self.logger.log(level,message,context))
        
    
    def wrapCallback(self,route: str,filters: List[IFilter]):
        wrappedCallback = WrappedCallback()
        wrappedCallback.filters = filters
        wrappedCallback.id = self.createUUID()
        wrappedCallback.instanceServiceName = self.config.instanceServiceName
        wrappedCallback.sessionId = self.id
        wrappedCallback.instanceId = self.config.instanceId
        wrappedCallback.path = route
        return wrappedCallback
    
    def constructCommandHeaders(self):
        headers = {}
        headers["traceId"] = self.createUUID()
        headers["instanceId"] = self.config.instanceId
        headers["sessionId"] = self.id
        headers["apiAccountId"] = self.config.apiAccountId
        headers["apiApplicationId"] = self.config.apiApplicationId
        headers["applicationName"] = self.config.instanceServiceName
        headers["applicationId"] = self.config.applicationId
        return headers
    
    def constructRequestHeaders(self,useBasicAuth: bool = False):
        headers = {}
        headers["X-Neru-SessionId"] = self.id
        headers["X-Neru-ApiAccountId"] = self.config.apiAccountId
        headers["X-Neru-ApiApplicationId"] = self.config.apiApplicationId
        headers["X-Neru-InstanceId"] = self.config.instanceId
        headers["X-Neru-TraceId"] = self.bridge.uuid()
        headers["Content-Type"] = "application/json"
        token = self.getToken()
        headers["Authorization"] = f'Bearer {token}'
        return headers
    
    async def request(self,params: IRequestParams[T]):
        try:
            result = await self.bridge.request(params)
            if params.responseType is RESPONSE_TYPE.STREAM:
                self.logStreamResponse(params)
            
            elif params.dataType is DATA_TYPE.FORM_DATA:
                self.logFormData(params,result)
            
            else: 
                self.logResponse(params,result)
            
            return result
        
        except Exception as e:
            self.logError(params,self.bridge.getErrorMessage(e))
            raise e
        
    
    def logStreamResponse(self,params: IRequestParams[T]):
        context = LogContext(params.url,None,"Stream response received")
        self.log(LOG_LEVEL.INFO,f'Sending {params.method} to {params.url}',context)
    
    def logFormData(self,params: IRequestParams[T],result: K):
        context = LogContext(params.url,"form-data is sent",self.bridge.jsonStringify(result))
        self.log(LOG_LEVEL.INFO,f'Sending {params.method} to {params.url}',context)
    
    def logResponse(self,params: IRequestParams[T],result: K):
        context = LogContext(params.url,self.bridge.jsonStringify(params.data),self.bridge.jsonStringify(result))
        self.log(LOG_LEVEL.INFO,f'Sending {params.method} to {params.url}',context)
    
    def logError(self,params: IRequestParams[T],message: str):
        context = LogContext(params.url,self.bridge.jsonStringify(params.data),message)
        self.log(LOG_LEVEL.ERROR,f'Error while sending a {params.method} request to {params.url}',context)
    
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
