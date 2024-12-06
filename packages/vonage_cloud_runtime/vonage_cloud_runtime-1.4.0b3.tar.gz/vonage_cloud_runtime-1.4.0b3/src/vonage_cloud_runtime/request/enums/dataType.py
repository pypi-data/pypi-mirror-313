from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class DATA_TYPE:
    FORM_DATA = "form-data"
