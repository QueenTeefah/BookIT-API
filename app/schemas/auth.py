from pydantic import BaseModel, EmailStr, ConfigDict ,field_validator
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None

class TokenPayload(BaseModel):
    sub: int
    exp: int
    jti: Optional[str] = None

class RegisterIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: EmailStr
    password: str
    

    @field_validator('password')
    def password_max_72_bytes(cls, v: str) -> str:
        if len(v.encode('utf-8')) > 72:
            raise ValueError('password too long: must be at most 72 bytes when UTF-8 encoded (bcrypt limit)')
        return v

class LoginIn(BaseModel):
    email: EmailStr
    password: str
