from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.services.config.IConfig import IConfig
from vonage_cloud_runtime.services.jwt.IJwt import IJWT
from vonage_cloud_runtime.services.jwt.contracts.acl import Acl
from vonage_cloud_runtime.services.jwt.contracts.ICreateVonageTokenParams import ICreateVonageTokenParams
from vonage_cloud_runtime.services.jwt.contracts.vcrJWTPayload import VCRJWTPayload
from vonage_cloud_runtime.services.jwt.contracts.vonageJWTPayload import VonageJWTPayload
from vonage_cloud_runtime.services.jwt.enums.algorithm import ALGORITHM

@dataclass
class JWT(IJWT):
    config: IConfig
    bridge: IBridge
    _token: str = field(default = None)
    ttl: int = field(default = 300)
    def __init__(self,bridge: IBridge,config: IConfig):
        self.bridge = bridge
        self.config = config
    
    def getToken(self):
        try:
            if self._token is None or self.isExpired():
                exp = self.bridge.getSystemTime() + self.ttl
                self._token = self.createVCRToken(exp)
            
            return self._token
        
        except Exception as e:
            raise self.bridge.createSdkError("getToken:" + self.bridge.getErrorMessage(e))
        
    
    def isExpired(self):
        nowInSeconds = self.bridge.getSystemTime()
        twentySeconds = 20
        payload = self.bridge.jwtDecode(self._token)
        return payload["exp"] - twentySeconds <= nowInSeconds
    
    def createVCRToken(self,exp: int):
        p = VCRJWTPayload()
        p.api_application_id = self.config.apiApplicationId
        p.api_account_id = self.config.apiAccountId
        p.exp = exp
        p.sub = self.config.instanceServiceName
        return self.bridge.jwtSign(p,self.config.privateKey,ALGORITHM.RS256)
    
    def createVonageToken(self,params: ICreateVonageTokenParams):
        jwtPayload = VonageJWTPayload()
        jwtPayload.iat = self.bridge.getSystemTime()
        jwtPayload.exp = params.exp
        jwtPayload.application_id = self.config.apiApplicationId
        jwtPayload.jti = self.bridge.uuid()
        if params.aclPaths:
            jwtPayload.acl = Acl()
            jwtPayload.acl.paths = params.aclPaths
        
        if params.subject:
            jwtPayload.sub = params.subject
        
        return self.bridge.jwtSign(jwtPayload,self.config.privateKey,ALGORITHM.RS256)
    
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
