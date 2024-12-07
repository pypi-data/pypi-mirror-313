from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class WEBHOOK_EVENT_TYPE:
    TEXT = "text"
    IMAGE = "IMAGE"
    VIDEO = "video"
    FILE = "file"
    AUDIO = "audio"
    REPLY = "reply"
    UNSUPPORTED = "unsupported"
    VCARD = "vcard"
