from pydantic import BaseModel

class Lead(BaseModel):
    name: str
    phone: str
    city: str
    purpose: str
