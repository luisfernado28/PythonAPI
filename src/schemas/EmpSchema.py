from pydantic import BaseModel, Field
from enum import Enum

class EmployeeType(Enum):
    ADMIN = "admin"
    CLIENT = "client"

class Employee(BaseModel):
    id: int = Field(primary_key=True,gt=0)
    name: str = Field(min_length=1, max_length=100)
    last_name: str = Field( min_length=1, max_length=100)
    email: str = Field(pattern=r".+@example\.com$")
    password: str = Field(min_length=8, max_length=200,repr=False)
    user_type: EmployeeType

class EmployeeResponse(BaseModel):
    name: str
    last_name: str
    email: str
    user_type: EmployeeType

class UserAuth(BaseModel):
    email: str = Field(pattern=r".+@example\.com$")
    password: str = Field(min_length=1, max_length=200, repr=False)

class UserOut(BaseModel):
    email: str
    id: int
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"