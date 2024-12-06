from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.scheduler.enums.schedulerAction import SCHEDULER_ACTION
from vonage_cloud_runtime.providers.scheduler.IScheduler import IScheduler
from vonage_cloud_runtime.providers.scheduler.contracts.startAtPayload import StartAtPayload
from vonage_cloud_runtime.providers.scheduler.contracts.schedulerPayload import SchedulerPayload
from vonage_cloud_runtime.providers.scheduler.contracts.IStartAtParams import IStartAtParams
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.scheduler.contracts.listAllSchedulersResponse import ListAllSchedulersResponse
from vonage_cloud_runtime.providers.scheduler.contracts.getSchedulerResponse import GetSchedulerResponse
from vonage_cloud_runtime.providers.scheduler.contracts.listAllPayload import ListAllPayload
from vonage_cloud_runtime.providers.scheduler.contracts.IListAllPayload import IListAllPayload
from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.providers.scheduler.contracts.IStartAtPayload import IStartAtPayload
from vonage_cloud_runtime.providers.scheduler.contracts.schedulerIDResponse import SchedulerIDResponse
from vonage_cloud_runtime.providers.scheduler.contracts.ISchedulePayload import ISchedulePayload
T = TypeVar('T')
@dataclass
class Scheduler(IScheduler):
    url: str
    bridge: IBridge
    session: ISession
    apiVersion: str = field(default = "v2")
    provider: str = field(default = "vonage-scheduler")
    def __init__(self,session: ISession):
        self.session = session
        self.bridge = session.bridge
    
    async def startAt(self,params: IStartAtParams[T]):
        if params.id is not None and self.bridge.testRegEx(params.id,"^[a-zA-Z0-9][a-zA-Z0-9-_]*$") is not True:
            raise self.bridge.createSdkError("startAt: The input does not match the required pattern ^[a-zA-Z0-9][a-zA-Z0-9-_]*$. Please enter a string that starts with a letter or a digit, and contains only letters, digits, hyphens, and underscores.")
        
        payload = StartAtPayload()
        payload.startAt = params.startAt
        payload.callback = self.session.wrapCallback(params.callback,[])
        if params.payload is not None:
            payload.payload = params.payload
        
        if params.interval is not None:
            payload.interval = params.interval
        
        if params.id is not None:
            payload.id = params.id
        
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = payload
        requestParams.url = self.session.config.getExecutionUrl(self.provider,f'{self.apiVersion}/{SCHEDULER_ACTION.CREATE}')
        requestParams.headers = self.session.constructRequestHeaders()
        response = await self.session.request(requestParams)
        return response["id"]
    
    async def list(self,size: int = 10,cursor: str = None):
        payload = ListAllPayload(size,cursor)
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = payload
        requestParams.url = self.session.config.getExecutionUrl(self.provider,f'{self.apiVersion}/{SCHEDULER_ACTION.LIST}')
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def get(self,scheduleId: str):
        payload = SchedulerPayload(scheduleId)
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = payload
        requestParams.url = self.session.config.getExecutionUrl(self.provider,f'{self.apiVersion}/{SCHEDULER_ACTION.GET}')
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def cancel(self,scheduleId: str):
        payload = SchedulerPayload(scheduleId)
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = payload
        requestParams.url = self.session.config.getExecutionUrl(self.provider,f'{self.apiVersion}/{SCHEDULER_ACTION.CANCEL}')
        requestParams.headers = self.session.constructRequestHeaders()
        await self.session.request(requestParams)
        return payload.id
    
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
