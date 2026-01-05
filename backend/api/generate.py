from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Content, Generation, User
from schemas import GenerationCreate, GenerationResponse, RegenerateRequest, BatchGenerationResponse
from services.ai_service import AIService
from api.auth import get_current_user

router = APIRouter()
ai_service = AIService()


@router.post("/repurpose", response_model=BatchGenerationResponse)
async def repurpose_content(
    request: GenerationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate repurposed content for multiple platforms"""
    
    # Get content
    content = db.query(Content).filter(
        Content.id == request.content_id,
        Content.user_id == current_user.id
    ).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Get brand voice if specified
    brand_voice_text = None
    if request.brand_voice_id:
        brand_voice = db.query(BrandVoice).filter(
            BrandVoice.id == request.brand_voice_id,
            BrandVoice.user_id == current_user.id
        ).first()
        if brand_voice:
            brand_voice_text = brand_voice.instructions
    
    # Generate content
    try:
        results = await ai_service.generate_repurposed_content(
            original_content=content.original_content,
            platforms=request.platforms,
            tone=request.tone,
            brand_voice=brand_voice_text
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating content: {str(e)}"
        )
    
    # Save generations
    generations = []
    for platform, generated_data in results.items():
        if "error" not in generated_data:
            generation = Generation(
                content_id=content.id,
                user_id=current_user.id,
                platform=platform,
                generated_text=str(generated_data),
                tone=request.tone,
                brand_voice_id=request.brand_voice_id,
                platform_metadata=generated_data
            )
            db.add(generation)
            generations.append(generation)
    
    db.commit()
    
    return {
        "content_id": content.id,
        "platform_results": results,
        "generations": generations
    }


@router.post("/regenerate/{generation_id}", response_model=GenerationResponse)
async def regenerate_content(
    generation_id: int,
    request: RegenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Regenerate a specific generated content"""
    
    # Get existing generation
    generation = db.query(Generation).filter(
        Generation.id == generation_id,
        Generation.user_id == current_user.id
    ).first()
    
    if not generation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generation not found"
        )
    
    # Get original content
    content = db.query(Content).filter(Content.id == generation.content_id).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Original content not found"
        )
    
    # Use new tone if provided, otherwise use existing
    tone = request.tone or generation.tone
    
    # Get brand voice if exists
    brand_voice_text = None
    if generation.brand_voice_id:
        from models import BrandVoice
        brand_voice = db.query(BrandVoice).filter(
            BrandVoice.id == generation.brand_voice_id
        ).first()
        if brand_voice:
            brand_voice_text = brand_voice.instructions
    
    # Regenerate
    try:
        results = await ai_service.generate_repurposed_content(
            original_content=content.original_content,
            platforms=[generation.platform],
            tone=tone,
            brand_voice=brand_voice_text
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error regenerating content: {str(e)}"
        )
    
    # Update generation
    generation.generated_text = str(results.get(generation.platform, {}))
    generation.tone = tone
    generation.platform_metadata = results.get(generation.platform, {})
    
    db.commit()
    db.refresh(generation)
    
    return generation


@router.get("/history", response_model=List[GenerationResponse])
async def get_generation_history(
    skip: int = 0,
    limit: int = 50,
    platform: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get generation history"""
    
    query = db.query(Generation).filter(Generation.user_id == current_user.id)
    
    if platform:
        query = query.filter(Generation.platform == platform)
    
    generations = query.offset(skip).limit(limit).all()
    
    return generations


@router.get("/{generation_id}", response_model=GenerationResponse)
async def get_generation(
    generation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific generation"""
    
    generation = db.query(Generation).filter(
        Generation.id == generation_id,
        Generation.user_id == current_user.id
    ).first()
    
    if not generation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generation not found"
        )
    
    return generation


@router.delete("/{generation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_generation(
    generation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete generation"""
    
    generation = db.query(Generation).filter(
        Generation.id == generation_id,
        Generation.user_id == current_user.id
    ).first()
    
    if not generation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generation not found"
        )
    
    db.delete(generation)
    db.commit()
    
    return None
