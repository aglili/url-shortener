from pydantic import BaseModel,HttpUrl



class LongURL(BaseModel):
    url: HttpUrl

class ShortenURLResponse(BaseModel):
    short_url: HttpUrl
    url: HttpUrl