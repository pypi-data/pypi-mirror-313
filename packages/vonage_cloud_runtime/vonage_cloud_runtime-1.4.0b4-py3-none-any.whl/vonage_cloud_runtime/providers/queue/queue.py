from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.queue.IQueue import IQueue
from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.services.config.IConfig import IConfig
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.queue.contracts.ICreateQueueOptions import ICreateQueueOptions
from vonage_cloud_runtime.providers.queue.contracts.createQueuePayload import CreateQueuePayload
from vonage_cloud_runtime.providers.queue.contracts.queueRate import QueueRate
from vonage_cloud_runtime.providers.queue.contracts.ICreateQueuePayload import ICreateQueuePayload
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.providers.queue.contracts.queueDetailsResponse import QueueDetailsResponse
from vonage_cloud_runtime.providers.queue.contracts.IUpdateQueueOptions import IUpdateQueueOptions
from vonage_cloud_runtime.providers.queue.contracts.updateQueuePayload import UpdateQueuePayload
from vonage_cloud_runtime.providers.queue.contracts.IUpdateQueuePayload import IUpdateQueuePayload
T = TypeVar('T')
@dataclass
class Queue(IQueue):
    session: ISession
    config: IConfig
    bridge: IBridge
    provider: str = field(default = "queue-service")
    def __init__(self,session: ISession):
        self.session = session
        self.bridge = session.bridge
        self.config = session.config
    
    async def createQueue(self,name: str,callback: str,options: ICreateQueueOptions):
        payload = CreateQueuePayload()
        payload.name = name
        payload.callback = self.session.wrapCallback(callback,[])
        payload.active = options.active
        payload.rate = QueueRate()
        payload.rate.maxInflight = options.maxInflight
        payload.rate.msgPerSecond = options.msgPerSecond
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = payload
        requestParams.url = self.config.getExecutionUrl(self.provider,"queue")
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def updateQueue(self,queueName: str,options: IUpdateQueueOptions):
        payload = UpdateQueuePayload()
        payload.rate = QueueRate()
        payload.rate.maxInflight = options.maxInflight
        payload.rate.msgPerSecond = options.msgPerSecond
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = payload
        requestParams.url = self.config.getExecutionUrl(self.provider,f'queue/{queueName}')
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def list(self):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.GET
        requestParams.data = None
        requestParams.url = self.config.getExecutionUrl(self.provider,"queue")
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def getQueueDetails(self,name: str):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.GET
        requestParams.data = None
        requestParams.url = self.config.getExecutionUrl(self.provider,f'queue/{name}')
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def deleteQueue(self,name: str):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.DEL
        requestParams.data = None
        requestParams.url = self.config.getExecutionUrl(self.provider,f'queue/{name}')
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def pauseQueue(self,name: str):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.PUT
        requestParams.data = None
        requestParams.url = self.config.getExecutionUrl(self.provider,f'queue/{name}/pause')
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def resumeQueue(self,name: str):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.PUT
        requestParams.data = None
        requestParams.url = self.config.getExecutionUrl(self.provider,f'queue/{name}/resume')
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def enqueue(self,name: str,data: List[T]):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = data
        requestParams.url = self.config.getExecutionUrl(self.provider,f'queue/{name}/enqueue')
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def enqueueSingle(self,name: str,data: T):
        await self.enqueue(name,[data])
    
    async def deadLetterList(self,name: str):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.GET
        requestParams.data = None
        requestParams.url = self.config.getExecutionUrl(self.provider,f'queue/{name}/deadletter')
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def deadLetterDequeue(self,name: str,count: int = 1):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = None
        requestParams.url = self.config.getExecutionUrl(self.provider,f'queue/{name}/deadletter/pop',{"count": self.bridge.jsonStringify(count)})
        requestParams.headers = self.session.constructRequestHeaders()
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
