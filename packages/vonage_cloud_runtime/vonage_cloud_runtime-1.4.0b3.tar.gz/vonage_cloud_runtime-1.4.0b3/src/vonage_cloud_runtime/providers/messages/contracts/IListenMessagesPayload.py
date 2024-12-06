from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.session.contracts.IPayloadWithCallback import IPayloadWithCallback
from vonage_cloud_runtime.providers.messages.contracts.IMessageContact import IMessageContact
from vonage_cloud_runtime.session.contracts.IWrappedCallback import IWrappedCallback


#interface
class IListenMessagesPayload(IPayloadWithCallback):
    from_:IMessageContact
    to:IMessageContact
    callback:IWrappedCallback
