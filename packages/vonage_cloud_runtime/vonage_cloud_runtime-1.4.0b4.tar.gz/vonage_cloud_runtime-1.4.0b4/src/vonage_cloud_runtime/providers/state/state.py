from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.state.IState import IState
from vonage_cloud_runtime.providers.state.contracts.IStateCommand import IStateCommand
from vonage_cloud_runtime.providers.state.contracts.stateCommand import StateCommand
from vonage_cloud_runtime.providers.state.enums.stateOperations import StateOperations
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.providers.state.enums.expireOption import EXPIRE_OPTION
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.providers.state.enums.fullText.IndexType import IndexType
from vonage_cloud_runtime.providers.state.contracts.fullText.createIndexOptions import CreateIndexOptions
from vonage_cloud_runtime.providers.state.enums.fullText.searchOptions import SearchOptions
T = TypeVar('T')
@dataclass
class State(IState):
    session: ISession
    bridge: IBridge
    url: str
    namespace: str
    provider: str = field(default = "client-persistence-api")
    def __init__(self,session: ISession,namespace: str = None):
        self.bridge = session.bridge
        self.url = session.config.getExecutionUrl(self.provider)
        if namespace is None:
            self.namespace = f'state:{session.id}'
        
        else: 
            self.namespace = namespace
        
        self.session = session
    
    def createCommand(self,op: str,key: str,args: List[str]):
        return StateCommand(op,self.namespace,key,args)
    
    async def executeCommand(self,command: IStateCommand):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.url = self.url
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.data = command
        return await self.session.request(requestParams)
    
    async def set(self,key: str,value: T):
        payload = []
        payload.append(self.bridge.jsonStringify(value))
        command = self.createCommand(StateOperations.SET,key,payload)
        return await self.executeCommand(command)
    
    async def get(self,key: str):
        payload = []
        command = self.createCommand(StateOperations.GET,key,payload)
        result = await self.executeCommand(command)
        if result is not None and result != "":
            return self.bridge.jsonParse(result)
        
        return None
    
    async def delete(self,key: str):
        payload = []
        command = self.createCommand(StateOperations.DEL,key,payload)
        return await self.executeCommand(command)
    
    async def increment(self,key: str,value: int):
        args = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.INCRBY,key,args)
        response = await self.executeCommand(command)
        return self.bridge.jsonParse(response)
    
    async def decrement(self,key: str,value: int):
        args = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.DECRBY,key,args)
        response = await self.executeCommand(command)
        return self.bridge.jsonParse(response)
    
    async def expire(self,key: str,seconds: int,option: EXPIRE_OPTION = None):
        args = [self.bridge.jsonStringify(seconds)]
        if option is not None:
            args.append(option)
        
        command = self.createCommand(StateOperations.EXPIRE,key,args)
        return await self.executeCommand(command)
    
    async def mapDelete(self,htable: str,keys: List[str]):
        command = self.createCommand(StateOperations.HDEL,htable,keys)
        return await self.executeCommand(command)
    
    async def mapExists(self,htable: str,key: str):
        payload = [key]
        command = self.createCommand(StateOperations.HEXISTS,htable,payload)
        return await self.executeCommand(command)
    
    async def mapGetAll(self,htable: str):
        payload = []
        command = self.createCommand(StateOperations.HGETALL,htable,payload)
        response = await self.executeCommand(command)
        result = {}
        for i in range(0,response.__len__(),2):
            result[response[i]] = response[i + 1]
        
        return result
    
    async def mapGetMultiple(self,htable: str,keys: List[str]):
        command = self.createCommand(StateOperations.HMGET,htable,keys)
        response = await self.executeCommand(command)
        result = []
        for i in range(0,response.__len__()):
            result.append(response[i])
        
        return result
    
    async def mapGetValues(self,htable: str):
        payload = []
        command = self.createCommand(StateOperations.HVALS,htable,payload)
        response = await self.executeCommand(command)
        result = []
        for i in range(0,response.__len__()):
            result.append(response[i])
        
        return result
    
    async def mapGetValue(self,htable: str,key: str):
        payload = [key]
        command = self.createCommand(StateOperations.HGET,htable,payload)
        return await self.executeCommand(command)
    
    async def mapSet(self,htable: str,keyValuePairs: Dict[str,str]):
        payload = []
        keys = self.bridge.getObjectKeys(keyValuePairs)
        for i in range(0,keys.__len__()):
            payload.append(keys[i])
            payload.append(keyValuePairs[keys[i]])
        
        command = self.createCommand(StateOperations.HSET,htable,payload)
        return await self.executeCommand(command)
    
    async def mapIncrement(self,htable: str,key: str,value: int):
        payload = [key,self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.HINCRBY,htable,payload)
        return await self.executeCommand(command)
    
    async def mapLength(self,htable: str):
        payload = []
        command = self.createCommand(StateOperations.HLEN,htable,payload)
        return await self.executeCommand(command)
    
    async def mapScan(self,htable: str,cursor: str,pattern: str = None,count: int = None):
        payload = []
        payload.append(cursor)
        if pattern is not None:
            payload.append("MATCH")
            payload.append(pattern)
        
        if count is not None:
            if count <= 0:
                raise self.bridge.createSdkError(f'mapScan: count must be greater than 0')
            
            payload.append("COUNT")
            payload.append(self.bridge.jsonStringify(count))
        
        command = self.createCommand(StateOperations.HSCAN,htable,payload)
        return await self.executeCommand(command)
    
    async def listAppend(self,list: str,value: T):
        payload = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.RPUSH,list,payload)
        return await self.executeCommand(command)
    
    async def listEndPop(self,list: str,count: int = 1):
        args = [self.bridge.jsonStringify(count)]
        command = self.createCommand(StateOperations.RPOP,list,args)
        response = await self.executeCommand(command)
        return self.parseResponse(response)
    
    async def listPrepend(self,list: str,value: T):
        payload = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LPUSH,list,payload)
        return await self.executeCommand(command)
    
    async def listStartPop(self,list: str,count: int = 1):
        args = [self.bridge.jsonStringify(count)]
        command = self.createCommand(StateOperations.LPOP,list,args)
        response = await self.executeCommand(command)
        return self.parseResponse(response)
    
    async def listRemove(self,list: str,value: T,count: int = 0):
        args = [self.bridge.jsonStringify(count),self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LREM,list,args)
        return await self.executeCommand(command)
    
    async def listLength(self,list: str):
        payload = []
        command = self.createCommand(StateOperations.LLEN,list,payload)
        return await self.executeCommand(command)
    
    async def listRange(self,list: str,startPos: int = 0,endPos: int = -1):
        args = [self.bridge.jsonStringify(startPos),self.bridge.jsonStringify(endPos)]
        command = self.createCommand(StateOperations.LRANGE,list,args)
        response = await self.executeCommand(command)
        return self.parseResponse(response)
    
    async def listTrim(self,list: str,startPos: int,endPos: int):
        args = [self.bridge.jsonStringify(startPos),self.bridge.jsonStringify(endPos)]
        command = self.createCommand(StateOperations.LTRIM,list,args)
        return await self.executeCommand(command)
    
    async def listInsert(self,list: str,before: bool,pivot: T,value: T):
        direction = "AFTER"
        if before is True:
            direction = "BEFORE"
        
        args = [direction,self.bridge.jsonStringify(pivot),self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LINSERT,list,args)
        return await self.executeCommand(command)
    
    async def listIndex(self,list: str,position: int):
        args = [self.bridge.jsonStringify(position)]
        command = self.createCommand(StateOperations.LINDEX,list,args)
        response = await self.executeCommand(command)
        return self.bridge.jsonParse(response)
    
    async def listSet(self,list: str,position: int,value: T):
        args = [self.bridge.jsonStringify(position),self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LSET,list,args)
        return await self.executeCommand(command)
    
    async def createIndex(self,name: str,options: CreateIndexOptions):
        args = []
        if options.on is not None:
            args.append("ON")
            args.append(options.on)
        
        else: 
            args.append("ON")
            args.append(IndexType.HASH)
        
        args.append("PREFIX")
        args.append(self.bridge.jsonStringify(options.prefix.count))
        for i in range(0,options.prefix.prefixes.__len__()):
            args.append(options.prefix.prefixes[i])
        
        if options.filter is not None:
            args.append("FILTER")
            args.append(options.filter)
        
        if options.language is not None:
            args.append("LANGUAGE")
            args.append(options.language)
        
        if options.languageField is not None:
            args.append("LANGUAGE_FIELD")
            args.append(options.languageField)
        
        if options.score is not None:
            args.append("SCORE")
            args.append(self.bridge.jsonStringify(options.score))
        
        if options.scoreField is not None:
            args.append("SCORE_FIELD")
            args.append(options.scoreField)
        
        if options.payloadField is not None:
            args.append("PAYLOAD_FIELD")
            args.append(options.payloadField)
        
        if options.maxTextFields:
            args.append("MAXTEXTFIELDS")
        
        if options.temporary is not None:
            args.append("TEMPORARY")
            args.append(self.bridge.jsonStringify(options.temporary))
        
        if options.noOffsets:
            args.append("NOOFFSETS")
        
        if options.noHl:
            args.append("NOHL")
        
        if options.noFields:
            args.append("NOFIELDS")
        
        if options.noFreqs:
            args.append("NOFREQS")
        
        if options.stopwords is not None:
            args.append("STOPWORDS")
            args.append(self.bridge.jsonStringify(options.stopwords.count))
            for i in range(0,options.stopwords.stopwords.__len__()):
                args.append(options.stopwords.stopwords[i])
            
        
        if options.skipInitialScan:
            args.append("SKIPINITIALSCAN")
        
        args.append("SCHEMA")
        for i in range(0,options.schema.__len__()):
            field = options.schema[i]
            args.append(field.fieldName)
            if field.alias is not None:
                args.append("AS")
                args.append(field.alias)
            
            args.append(field.type_)
            if field.sortable:
                args.append("SORTABLE")
            
            if field.unf:
                args.append("UNF")
            
            if field.noIndex:
                args.append("NOINDEX")
            
        
        command = self.createCommand(StateOperations.FTCREATE,name,args)
        return await self.executeCommand(command)
    
    async def search(self,index: str,query: str,options: SearchOptions = None):
        args = []
        args.append(query)
        if options is not None:
            if options.noContent is True:
                args.append("NOCONTENT")
            
            if options.verbatim is True:
                args.append("VERBATIM")
            
            if options.noStopwords is True:
                args.append("NOSTOPWORDS")
            
            if options.withScores is True:
                args.append("WITHSCORES")
            
            if options.withPayloads is True:
                args.append("WITHPAYLOADS")
            
            if options.withSortKeys is True:
                args.append("WITHSORTKEYS")
            
            if options.filters is not None:
                for i in range(0,options.filters.__len__()):
                    filter = options.filters[i]
                    args.append("FILTER")
                    args.append(filter.numericField)
                    args.append(self.bridge.jsonStringify(filter.min))
                    args.append(self.bridge.jsonStringify(filter.max))
                
            
            if options.geoFilters is not None:
                for i in range(0,options.geoFilters.__len__()):
                    geoFilter = options.geoFilters[i]
                    args.append("GEOFILTER")
                    args.append(geoFilter.geoField)
                    args.append(self.bridge.jsonStringify(geoFilter.lon))
                    args.append(self.bridge.jsonStringify(geoFilter.lat))
                    args.append(self.bridge.jsonStringify(geoFilter.radius))
                    args.append(geoFilter.unit)
                
            
            if options.inKeys is not None:
                args.append("INKEYS")
                args.append(self.bridge.jsonStringify(options.inKeys.count))
                for i in range(0,options.inKeys.keys.__len__()):
                    args.append(options.inKeys.keys[i])
                
            
            if options.inFields is not None:
                args.append("INFIELDS")
                args.append(self.bridge.jsonStringify(options.inFields.count))
                for i in range(0,options.inFields.fields.__len__()):
                    args.append(options.inFields.fields[i])
                
            
            if options.return_ is not None:
                args.append("RETURN")
                args.append(self.bridge.jsonStringify(options.return_.count))
                for i in range(0,options.return_.fields.__len__()):
                    field = options.return_.fields[i]
                    args.append(field.identifier)
                    if field.property is not None:
                        args.append("AS")
                        args.append(field.property)
                    
                
            
            if options.summarize is not None:
                args.append("SUMMARIZE")
                if options.summarize.fields is not None:
                    args.append("FIELDS")
                    args.append(self.bridge.jsonStringify(options.summarize.fields.__len__()))
                    for i in range(0,options.summarize.fields.__len__()):
                        args.append(options.summarize.fields[i])
                    
                
                if options.summarize.frags is not None:
                    args.append("FRAGS")
                    args.append(self.bridge.jsonStringify(options.summarize.frags))
                
                if options.summarize.len is not None:
                    args.append("LEN")
                    args.append(self.bridge.jsonStringify(options.summarize.len))
                
                if options.summarize.separator is not None:
                    args.append("SEPARATOR")
                    args.append(options.summarize.separator)
                
            
            if options.highlight is not None:
                args.append("HIGHLIGHT")
                if options.highlight.fields is not None:
                    args.append("FIELDS")
                    args.append(self.bridge.jsonStringify(options.highlight.fields.__len__()))
                    for i in range(0,options.highlight.fields.__len__()):
                        args.append(options.highlight.fields[i])
                    
                
                if options.highlight.tags is not None:
                    args.append("TAGS")
                    args.append(options.highlight.tags.open)
                    args.append(options.highlight.tags.close)
                
            
            if options.slop is not None:
                args.append("SLOP")
                args.append(self.bridge.jsonStringify(options.slop))
            
            if options.timeout is not None:
                args.append("TIMEOUT")
                args.append(self.bridge.jsonStringify(options.timeout))
            
            if options.inorder is True:
                args.append("INORDER")
            
            if options.language is not None:
                args.append("LANGUAGE")
                args.append(options.language)
            
            if options.expander is not None:
                args.append("EXPANDER")
                args.append(options.expander)
            
            if options.scorer is not None:
                args.append("SCORER")
                args.append(options.scorer)
            
            if options.explainScore is True:
                args.append("EXPLAINSCORE")
            
            if options.payload is not None:
                args.append("PAYLOAD")
                args.append(options.payload)
            
            if options.sortBy is not None:
                args.append("SORTBY")
                args.append(options.sortBy.field)
                if options.sortBy.order is not None:
                    args.append(options.sortBy.order)
                
            
            if options.limit is not None:
                args.append("LIMIT")
                args.append(self.bridge.jsonStringify(options.limit.offset))
                args.append(self.bridge.jsonStringify(options.limit.num))
            
            if options.params is not None:
                args.append("PARAMS")
                args.append(self.bridge.jsonStringify(options.params.__len__()))
                for i in range(0,options.params.__len__()):
                    param = options.params[i]
                    args.append(param.name)
                    args.append(param.value)
                
            
            if options.dialect is not None:
                args.append("DIALECT")
                args.append(options.dialect)
            
        
        command = self.createCommand(StateOperations.FTSEARCH,index,args)
        return await self.executeCommand(command)
    
    async def dropIndex(self,index: str,deleteDocs: bool = None):
        args = []
        if deleteDocs is True:
            args.append("DD")
        
        command = self.createCommand(StateOperations.FTDROPINDEX,index,args)
        return await self.executeCommand(command)
    
    def parseResponse(self,response: List[str]):
        result = []
        if response is not None:
            for i in range(0,response.__len__()):
                result.append(self.bridge.jsonParse(response[i]))
            
        
        return result
    
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
