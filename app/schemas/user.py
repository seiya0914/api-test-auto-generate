from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., description="ユーザー名")
    email: EmailStr = Field(..., description="メールアドレス")
    full_name: Optional[str] = Field(None, description="氏名")
    department: Optional[str] = Field(None, description="部署名")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="ユーザー名")
    email: Optional[EmailStr] = Field(None, description="メールアドレス")
    full_name: Optional[str] = Field(None, description="氏名")
    department: Optional[str] = Field(None, description="部署名")


class UserInDB(UserBase):
    id: UUID = Field(..., description="ユーザーID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    department: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "username": "yamada_taro",
                "email": "taro.yamada@example.com",
                "full_name": "山田 太郎",
                "department": "営業部",
                "created_at": "2025-04-09T08:56:01",
                "updated_at": "2025-04-09T08:56:01"
            }
        }
