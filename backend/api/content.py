from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os

from database import get_db
from models import Content, User
from schemas import ContentCreate, ContentResponse, ContentUpdate
from services.content_service import ContentParser, FileHandler
from api.auth import get_current_user

router = APIRouter()
file_handler = FileHandler()


@router.post("/upload", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def upload_content(
    content_data: ContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload or input content"""
    
    original_content = content_data.original_content
    
    # If URL, extract content
    if content_data.content_type == "url":
        try:
            original_content = ContentParser.extract_from_url(content_data.original_content)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to extract content from URL: {str(e)}"
            )
    
    # Clean content
    original_content = ContentParser.clean_content(original_content)
    
    # Count words
    word_count = ContentParser.count_words(original_content)
    
    # Create content record
    content = Content(
        user_id=current_user.id,
        title=content_data.title,
        original_content=original_content,
        content_type=content_data.content_type,
        source_url=content_data.original_content if content_data.content_type == "url" else None,
        word_count=word_count
    )
    
    db.add(content)
    db.commit()
    db.refresh(content)
    
    return content


@router.post("/upload-file", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    title: str = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload file and extract content"""
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.txt', '.md', '.pdf', '.docx']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Allowed: .txt, .md, .pdf, .docx"
        )
    
    try:
        # Save file
        contents = await file.read()
        file_path = f"{current_user.id}/{file.filename}"
        full_path = await file_handler.save_uploaded_file(file_path, contents)
        
        # Extract text
        original_content = file_handler.extract_text_from_file(full_path)
        original_content = ContentParser.clean_content(original_content)
        
        # Create content record
        word_count = ContentParser.count_words(original_content)
        content = Content(
            user_id=current_user.id,
            title=title or file.filename,
            original_content=original_content,
            content_type="file",
            word_count=word_count
        )
        
        db.add(content)
        db.commit()
        db.refresh(content)
        
        return content
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/", response_model=List[ContentResponse])
async def list_content(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List user's content"""
    
    contents = db.query(Content).filter(
        Content.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return contents


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific content"""
    
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    return content


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    content_update: ContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update content"""
    
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    if content_update.title:
        content.title = content_update.title
    
    db.commit()
    db.refresh(content)
    
    return content


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete content"""
    
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    db.delete(content)
    db.commit()
    
    return None
