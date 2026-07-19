from pydantic import BaseModel, EmailStr, Field


class AuthorizationSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)