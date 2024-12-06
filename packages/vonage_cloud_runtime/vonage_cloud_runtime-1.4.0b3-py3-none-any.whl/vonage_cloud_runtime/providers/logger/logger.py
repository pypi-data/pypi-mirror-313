from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.services.config.IConfig import IConfig
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.logger.contracts.ILogContext import ILogContext
from vonage_cloud_runtime.providers.logger.ILogger import ILogger
from vonage_cloud_runtime.providers.logger.contracts.logAction import LogAction
from vonage_cloud_runtime.providers.logger.enums.sourceType import SOURCE_TYPE

@dataclass
class Logger(ILogger):
    url: str
    session: ISession
    bridge: IBridge
    config: IConfig
    provider: str = field(default = "logs-submission")
    def __init__(self,session: ISession):
        self.config = session.config
        self.bridge = session.bridge
        self.session = session
        self.url = self.config.getExecutionUrl(self.provider)
    
    def createLogAction(self,level: str,message: str,context: ILogContext = None):
        logAction = LogAction()
        logAction.id = self.bridge.uuid()
        logAction.api_application_id = self.config.apiApplicationId
        logAction.api_account_id = self.config.apiAccountId
        logAction.session_id = self.session.id
        logAction.timestamp = self.bridge.isoDate()
        logAction.log_level = level
        logAction.message = message
        logAction.source_type = SOURCE_TYPE.APPLICATION
        logAction.source_id = self.config.instanceServiceName
        logAction.instance_id = self.config.instanceId
        if context is not None:
            logAction.context = context
        
        return logAction
    
    async def log(self,level: str,message: str,context: ILogContext = None):
        logAction = self.createLogAction(level,message,context)
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.url = self.url
        requestParams.data = logAction
        requestParams.headers = self.session.constructRequestHeaders()
        await self.bridge.requestWithoutResponse(requestParams)
    
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
