from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, BrandVoice
from schemas import UserResponse, UserUpdate, BrandVoiceCreate, BrandVoiceResponse, BrandVoiceUpdate
from api.auth import get_current_user

router = APIRouter()


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    
    if user_update.username:
        current_user.username = user_update.username
    
    if user_update.plan:
        current_user.plan = user_update.plan
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.post("/brand-voice", response_model=BrandVoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_brand_voice(
    brand_voice_data: BrandVoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a brand voice template"""
    
    brand_voice = BrandVoice(
        user_id=current_user.id,
        name=brand_voice_data.name,
        instructions=brand_voice_data.instructions
    )
    
    db.add(brand_voice)
    db.commit()
    db.refresh(brand_voice)
    
    return brand_voice


@router.get("/brand-voices", response_model=List[BrandVoiceResponse])
async def get_brand_voices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's brand voice templates"""
    
    brand_voices = db.query(BrandVoice).filter(
        BrandVoice.user_id == current_user.id
    ).all()
    
    return brand_voices


@router.get("/brand-voice/{brand_voice_id}", response_model=BrandVoiceResponse)
async def get_brand_voice(
    brand_voice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific brand voice"""
    
    brand_voice = db.query(BrandVoice).filter(
        BrandVoice.id == brand_voice_id,
        BrandVoice.user_id == current_user.id
    ).first()
    
    if not brand_voice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand voice not found"
        )
    
    return brand_voice


@router.put("/brand-voice/{brand_voice_id}", response_model=BrandVoiceResponse)
async def update_brand_voice(
    brand_voice_id: int,
    brand_voice_update: BrandVoiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update brand voice"""
    
    brand_voice = db.query(BrandVoice).filter(
        BrandVoice.id == brand_voice_id,
        BrandVoice.user_id == current_user.id
    ).first()
    
    if not brand_voice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand voice not found"
        )
    
    if brand_voice_update.name:
        brand_voice.name = brand_voice_update.name
    
    if brand_voice_update.instructions:
        brand_voice.instructions = brand_voice_update.instructions
    
    if brand_voice_update.is_default is not None:
        brand_voice.is_default = brand_voice_update.is_default
    
    db.commit()
    db.refresh(brand_voice)
    
    return brand_voice


@router.delete("/brand-voice/{brand_voice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand_voice(
    brand_voice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete brand voice"""
    
    brand_voice = db.query(BrandVoice).filter(
        BrandVoice.id == brand_voice_id,
        BrandVoice.user_id == current_user.id
    ).first()
    
    if not brand_voice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand voice not found"
        )
    
    db.delete(brand_voice)
    db.commit()
    
    return None
