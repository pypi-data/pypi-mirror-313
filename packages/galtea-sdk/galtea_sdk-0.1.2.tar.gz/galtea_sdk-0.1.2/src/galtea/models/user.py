from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserRole(Enum):
    annotator = "annotator"
    owner = "owner"
    admin = "admin"

class UserInput(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole = Field(default=UserRole.annotator)
