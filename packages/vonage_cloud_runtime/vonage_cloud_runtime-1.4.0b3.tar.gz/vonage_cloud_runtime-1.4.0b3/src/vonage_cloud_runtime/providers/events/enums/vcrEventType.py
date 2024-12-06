from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class VCR_EVENT_TYPE:
    SESSION_DESTROY = "session_destroy"
    SESSION_CREATED = "session_created"
    APPLICATION_DEPLOYED = "application_deployed"
    INSTANCE_CREATED = "instance_created"
    INSTANCE_DESTROYED = "instance_destroyed"
    STATE_GET = "state_get"
    EVENT_SUBSCRIBED = "event_subscribed"
    EVENT_FIRED = "event_fired"
