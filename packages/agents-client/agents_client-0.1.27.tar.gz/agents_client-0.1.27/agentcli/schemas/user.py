from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class HealthCheck(BaseModel):
    status: str
    database: str
    timestamp: datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class APIKeyCreate(BaseModel):
    name: str

class APIKeyResponse(BaseModel):
    id: int
    key: str
    name: str
    created_at: datetime
    last_used: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool
    api_keys: List[APIKeyResponse] = []

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserRegistrationResponse(BaseModel):
    user: User
    api_key: str
    message: str

    class Config:
        from_attributes = True

class QuickAPIKeyResponse(BaseModel):
    api_key: str
    expires_in: int  # Time in seconds until key expires
    message: str
