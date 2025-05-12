from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID

class User(BaseModel):
    name: str
    surname: str
    date_of_birth: date
    login: str = Field(min_length=5)
    email: str = Field(min_length=7)
    
class UserCreate(User):
    password: str = Field(min_length=5)

class UserLogin(BaseModel):
    email: str = Field(min_length=7)
    password: str = Field(min_length=5)

class UserResponse(User):
    id: UUID

