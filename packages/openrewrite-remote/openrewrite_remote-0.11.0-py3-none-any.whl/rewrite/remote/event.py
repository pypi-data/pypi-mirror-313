from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EventType(Enum):
    NoChange = 0
    Update = 1
    Add = 2
    Delete = 3
    Move = 4
    StartList = 5
    EndList = 6


@dataclass(frozen=True)
class DiffEvent:
    event_type: EventType
    concrete_type: Optional[str] = None
    msg: Optional[any] = None
