from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class VCR_EVENT_SOURCE_TYPE:
    INSTANCE = "instance"
