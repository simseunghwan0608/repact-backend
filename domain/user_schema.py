from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    username: str
    password: str
    phone: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str
