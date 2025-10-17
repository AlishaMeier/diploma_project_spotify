from pydantic import BaseModel, EmailStr, Field

class UserData(BaseModel):
    id: int
    email: EmailStr
    first_name: str = Field(..., alias='first_name')
    last_name: str = Field(..., alias='last_name')
    avatar: str

class SingleUserResponse(BaseModel):
    data: UserData

class ListUsersResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[UserData]

class CreateUserRequest(BaseModel):
    name: str
    job: str

class CreateUserResponse(BaseModel):
    id: str  # API возвращает id как строку
    name: str
    job: str
    createdAt: str