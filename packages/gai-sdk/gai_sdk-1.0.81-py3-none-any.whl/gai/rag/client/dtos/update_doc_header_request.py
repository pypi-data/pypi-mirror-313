from pydantic import BaseModel
class UpdateDocHeaderRequestPydantic(BaseModel):
    FileName: str = None
    Source: str = None
    Abstract: str = None
    Authors: str = None
    Title: str = None
    Publisher: str = None
    PublishedDate: str = None
    Comments: str = None
    Keywords: str = None