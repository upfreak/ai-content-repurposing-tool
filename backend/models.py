from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    plan = Column(String(50), default="free")
    
    # Relationships
    contents = relationship("Content", back_populates="owner", cascade="all, delete-orphan")
    generations = relationship("Generation", back_populates="owner", cascade="all, delete-orphan")
    brand_voices = relationship("BrandVoice", back_populates="owner", cascade="all, delete-orphan")


class Content(Base):
    """Content model for storing original content"""
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    original_content = Column(Text, nullable=False)
    content_type = Column(String(50), nullable=False)  # text, url, file
    source_url = Column(String(500), nullable=True)
    word_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="contents")
    generations = relationship("Generation", back_populates="content", cascade="all, delete-orphan")


class Generation(Base):
    """Generated content for different platforms"""
    __tablename__ = "generations"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    platform = Column(String(50), nullable=False, index=True)  # twitter, linkedin, etc.
    generated_text = Column(Text, nullable=False)
    tone = Column(String(50), nullable=False)  # professional, casual, etc.
    brand_voice_id = Column(Integer, ForeignKey("brand_voices.id"), nullable=True)
    platform_metadata = Column(JSON, nullable=True)  # Additional platform-specific metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    content = relationship("Content", back_populates="generations")
    owner = relationship("User", back_populates="generations")
    brand_voice = relationship("BrandVoice")


class BrandVoice(Base):
    """User's brand voice templates"""
    __tablename__ = "brand_voices"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    instructions = Column(Text, nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="brand_voices")
