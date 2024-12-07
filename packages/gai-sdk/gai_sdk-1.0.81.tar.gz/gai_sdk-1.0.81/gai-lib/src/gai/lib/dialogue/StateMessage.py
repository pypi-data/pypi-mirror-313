from __future__ import annotations
from typing import List, Optional

class StateMessage:
    MessageOrder: int
    OwnerName: str
    Title: str
    StateOutput: str
    ChildMessages: Optional[List[StateMessage]]

    def __init__(self, MessageOrder: int, OwnerName: str, Title: str, StateOutput: str, ChildMessages: Optional[List[StateMessage]] = None):
        self.MessageOrder = MessageOrder
        self.OwnerName = OwnerName
        self.Title = Title
        self.StateOutput = StateOutput
        self.ChildMessages = ChildMessages if ChildMessages is not None else []

    def to_dict(self) -> dict:
        """Serialize the StateMessage object to a dictionary."""
        return {
            'MessageOrder': self.MessageOrder,
            'OwnerName': self.OwnerName,
            'Title': self.Title,
            'StateOutput': self.StateOutput,
            'ChildMessages': [child.to_dict() for child in self.ChildMessages]
        }

    def __repr__(self) -> str:
        """Return the dictionary representation of the object as a string."""
        return str(self.to_dict())