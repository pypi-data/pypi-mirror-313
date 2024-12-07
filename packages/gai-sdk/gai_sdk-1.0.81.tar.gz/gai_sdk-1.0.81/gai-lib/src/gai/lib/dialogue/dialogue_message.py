from typing import Optional,Any
from pydantic import BaseModel

class DialogueMessage(BaseModel):
    Id: str
    DialogueId: str     # ParentID
    Order: int
    OwnerId: Optional[str] = None
    Role: str
    Name: Optional[str] = None
    Content: str
    Monologue: Optional[Any] = None  # JSON fields can be represented by Any type
    Timestamp: int
    ImageUrl: Optional[Any] = None  # Do not load this field from the database
