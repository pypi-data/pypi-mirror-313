from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class VOICE_ACTION:
    VAPI_SUBSCRIBE_INBOUND_CALL = "vapi-subscribe-inbound-call"
    VAPI_SUBSCRIBE_EVENT = "vapi-subscribe-event"
