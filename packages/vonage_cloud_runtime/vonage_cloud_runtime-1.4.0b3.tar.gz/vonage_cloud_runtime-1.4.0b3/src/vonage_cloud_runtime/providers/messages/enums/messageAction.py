from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class MESSAGE_ACTION:
    SUBSCRIBE_INBOUND_MESSAGES = "subscribe-inbound-messages"
    SUBSCRIBE_INBOUND_EVENTS = "subscribe-inbound-events"
    UNSUBSCRIBE_EVENTS = "unsubscribe-event"
