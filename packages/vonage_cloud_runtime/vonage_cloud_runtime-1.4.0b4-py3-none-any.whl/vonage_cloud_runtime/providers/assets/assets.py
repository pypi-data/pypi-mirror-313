from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.services.config.IConfig import IConfig
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.assets.IAssets import IAssets
from vonage_cloud_runtime.providers.assets.contracts.directoryPayload import DirectoryPayload
from vonage_cloud_runtime.providers.assets.contracts.removeAssetPayload import RemoveAssetPayload
from vonage_cloud_runtime.providers.assets.contracts.listAssetsPayload import ListAssetsPayload
from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.providers.assets.enums.assetsAction import ASSETS_ACTION
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.providers.assets.contracts.linkPayload import LinkPayload
from vonage_cloud_runtime.providers.assets.contracts.assetLinkResponse import AssetLinkResponse
from vonage_cloud_runtime.providers.assets.contracts.assetListResponse import AssetListResponse
from vonage_cloud_runtime.request.contracts.formDataObject import FormDataObject
from vonage_cloud_runtime.request.contracts.IFormDataObject import IFormDataObject
from vonage_cloud_runtime.request.enums.responseTypes import RESPONSE_TYPE
from vonage_cloud_runtime.providers.assets.enums.fileRetentionPeriod import FILE_RETENTION_PERIOD
from vonage_cloud_runtime.request.enums.dataType import DATA_TYPE

@dataclass
class Assets(IAssets):
    bridge: IBridge
    session: ISession
    config: IConfig
    provider: str = field(default = "vonage-assets")
    def __init__(self,session: ISession):
        self.session = session
        self.bridge = session.bridge
        self.config = session.config
    
    async def createDir(self,name: str):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = DirectoryPayload(name)
        requestParams.url = self.config.getExecutionUrl(self.provider,ASSETS_ACTION.MKDIR)
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def remove(self,remoteFilePath: str,recursive: bool = False):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = RemoveAssetPayload(remoteFilePath,recursive)
        requestParams.url = self.config.getExecutionUrl(self.provider,ASSETS_ACTION.REMOVE)
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def getRemoteFile(self,remoteFilePath: str):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.GET
        requestParams.url = self.config.getExecutionUrl(self.provider,ASSETS_ACTION.BINARY,{"key": remoteFilePath})
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.responseType = RESPONSE_TYPE.STREAM
        return await self.session.request(requestParams)
    
    async def generateLink(self,remoteFilePath: str,duration: str = "5m"):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = LinkPayload(remoteFilePath,duration)
        requestParams.url = self.config.getExecutionUrl(self.provider,ASSETS_ACTION.LINK)
        requestParams.headers = self.session.constructRequestHeaders()
        return await self.session.request(requestParams)
    
    async def uploadFiles(self,localFilePaths: List[str],remoteDir: str,retentionPeriod: FILE_RETENTION_PERIOD = None):
        streams = []
        for i in range(0,localFilePaths.__len__()):
            streams.append(self.bridge.createReadStream(localFilePaths[i]))
        
        await self.uploadData(streams,remoteDir,None,retentionPeriod)
        return
    
    async def uploadData(self,data: List[object],remoteDir: str,filenames: List[str] = None,retentionPeriod: FILE_RETENTION_PERIOD = None):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.dataType = DATA_TYPE.FORM_DATA
        requestParams.data = []
        for i in range(0,data.__len__()):
            formData = FormDataObject()
            formData.name = f'file[{i}]'
            formData.value = data[i]
            if filenames is not None and filenames[i] is not None:
                formData.filename = filenames[i]
            
            requestParams.data.append(formData)
        
        requestParams.url = self.config.getExecutionUrl(self.provider,ASSETS_ACTION.COPY,{"dst": remoteDir,"retention": retentionPeriod})
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.headers["Content-Type"] = "multipart/form-data"
        return await self.session.request(requestParams)
    
    async def list(self,remotePath: str,recursive: bool = False,limit: int = 1000):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.data = ListAssetsPayload(remotePath,recursive,limit)
        requestParams.url = self.config.getExecutionUrl(self.provider,ASSETS_ACTION.LIST)
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
