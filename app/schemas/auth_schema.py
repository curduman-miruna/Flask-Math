from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    phone_number: str
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
