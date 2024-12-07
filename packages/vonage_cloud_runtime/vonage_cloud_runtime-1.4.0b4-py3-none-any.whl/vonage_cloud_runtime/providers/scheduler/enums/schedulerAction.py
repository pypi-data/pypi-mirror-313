from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class SCHEDULER_ACTION:
    CREATE = "create"
    CANCEL = "cancel"
    LIST = "list"
    GET = "get"
