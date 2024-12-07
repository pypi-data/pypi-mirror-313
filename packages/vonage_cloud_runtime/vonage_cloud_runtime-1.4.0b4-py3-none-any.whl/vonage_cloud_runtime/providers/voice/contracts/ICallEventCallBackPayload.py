from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.session.contracts.IPayloadWithCallback import IPayloadWithCallback


#interface
class ICallEventCallBackPayload(IPayloadWithCallback):
    vapiId:str
    conversationId:str
