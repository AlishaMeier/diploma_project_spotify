from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    id: str
    display_name: str = Field(..., alias='display_name')
    email: str
    country: str