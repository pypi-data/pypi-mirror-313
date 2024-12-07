from pydantic import BaseModel,ConfigDict
from typing import List, Optional,Any

class DialoguePydantic(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Allows the model to work with ORM objects
    Id: str
    InitiatorId: str
    IsActive: bool
