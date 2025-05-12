from sqlmodel import SQLModel, Column, Field
from datetime import datetime, date
import uuid

class User(SQLModel, table=True):

    __tablename__ = 'Users'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, 
                     primary_key=True, nullable=False)
    name: str
    surname: str
    date_of_birth: date

    login: str = Field(unique=True)
    email: str = Field(unique=True)

    password_hash: str
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    