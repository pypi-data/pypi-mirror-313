from pydantic import BaseModel,ConfigDict
from typing import List, Optional,Any

class DialogueMessagePydantic(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Allows the model to work with ORM objects
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

