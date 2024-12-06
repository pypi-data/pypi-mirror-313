from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class CONVERSATION_ACTION:
    CONVERSATION_SUBSCRIBE_EVENT = "conversation-subscribe-event"
