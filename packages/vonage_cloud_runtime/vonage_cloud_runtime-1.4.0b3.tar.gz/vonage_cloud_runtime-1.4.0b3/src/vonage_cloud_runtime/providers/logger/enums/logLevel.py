from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class LOG_LEVEL:
    ERROR = "error"
    WARN = "warn"
    INFO = "info"
    DEBUG = "debug"
