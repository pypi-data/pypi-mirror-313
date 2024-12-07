from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class REQUEST_VERB:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DEL = "DELETE"
    HEAD = "HEAD"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
