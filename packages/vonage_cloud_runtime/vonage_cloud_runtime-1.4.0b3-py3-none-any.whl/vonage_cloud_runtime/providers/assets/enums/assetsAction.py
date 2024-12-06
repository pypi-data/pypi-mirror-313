from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class ASSETS_ACTION:
    MKDIR = "mkdir"
    REMOVE = "remove"
    GET = "get"
    LINK = "link"
    BINARY = "binary"
    DOWNLOAD = "download"
    COPY = "copy"
    LIST = "list"
