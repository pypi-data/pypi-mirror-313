from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class RESPONSE_TYPE:
    JSON = "json"
    TEXT = "text"
    STREAM = "stream"
    ARRAYBUFFER = "arraybuffer"
    BLOB = "blob"
