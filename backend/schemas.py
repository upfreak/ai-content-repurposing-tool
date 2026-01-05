from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    plan: str
    is_active: bool
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    plan: Optional[str] = None


# Token Schemas
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


# Content Schemas
class ContentCreate(BaseModel):
    title: Optional[str] = None
    original_content: str
    content_type: str  # text, url, file


class ContentResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    original_content: str
    content_type: str
    word_count: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ContentUpdate(BaseModel):
    title: Optional[str] = None


# Generation Schemas
class GenerationCreate(BaseModel):
    content_id: int
    platforms: List[str]
    tone: str = Field(..., min_length=3)
    brand_voice_id: Optional[int] = None


class GenerationResponse(BaseModel):
    id: int
    content_id: int
    platform: str
    generated_text: str
    tone: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class RegenerateRequest(BaseModel):
    generation_id: int
    tone: Optional[str] = None


# Brand Voice Schemas
class BrandVoiceCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    instructions: str = Field(..., min_length=10)


class BrandVoiceResponse(BaseModel):
    id: int
    user_id: int
    name: str
    instructions: str
    is_default: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class BrandVoiceUpdate(BaseModel):
    name: Optional[str] = None
    instructions: Optional[str] = None
    is_default: Optional[bool] = None


# Batch generation response
class BatchGenerationResponse(BaseModel):
    content_id: int
    platform_results: dict  # {platform: generated_text}
    generations: List[GenerationResponse]
