from pydantic import BaseModel,HttpUrl
from typing import Optional



class LongURL(BaseModel):
    url: str

class ShortenURLResponse(BaseModel):
    short_url: str
    url: str
    whatsapp: Optional[str] = None
    facebook: Optional[str] = None
    gmail: Optional[str] = None