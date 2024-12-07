from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class MonologueMessagePydantic(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Allows the model to work with ORM objects
    Order: int
    Name: str
    Role: str
    Title: str
    Content: str
    ChildMessages: Optional[List['MonologueMessagePydantic']] = []
    Timestamp: Optional[int] = None
