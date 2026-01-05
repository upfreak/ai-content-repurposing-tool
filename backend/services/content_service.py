import os
from pathlib import Path
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FileHandler:
    """Handle file uploads and content extraction"""
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        Path(self.upload_dir).mkdir(exist_ok=True)
    
    async def save_uploaded_file(self, file_path: str, content: bytes) -> str:
        """Save uploaded file and return path"""
        try:
            full_path = os.path.join(self.upload_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'wb') as f:
                f.write(content)
            
            return full_path
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from .txt file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading text file: {str(e)}")
            raise
    
    def extract_text_from_md(self, file_path: str) -> str:
        """Extract text from .md file"""
        return self.extract_text_from_txt(file_path)
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Error reading PDF: {str(e)}")
            raise
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from .docx file"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error reading DOCX: {str(e)}")
            raise
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from file based on extension"""
        ext = Path(file_path).suffix.lower()
        
        handlers = {
            '.txt': self.extract_text_from_txt,
            '.md': self.extract_text_from_md,
            '.pdf': self.extract_text_from_pdf,
            '.docx': self.extract_text_from_docx,
        }
        
        handler = handlers.get(ext)
        if not handler:
            raise ValueError(f"Unsupported file type: {ext}")
        
        return handler(file_path)


class ContentParser:
    """Parse and clean content from various sources"""
    
    @staticmethod
    def extract_from_url(url: str) -> Optional[str]:
        """Extract content from URL"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            logger.error(f"Error extracting from URL: {str(e)}")
            raise
    
    @staticmethod
    def clean_content(content: str) -> str:
        """Clean and normalize content"""
        # Remove extra whitespace
        content = ' '.join(content.split())
        return content.strip()
    
    @staticmethod
    def count_words(content: str) -> int:
        """Count words in content"""
        return len(content.split())
    
    @staticmethod
    def extract_key_points(content: str, max_points: int = 5) -> list:
        """Extract key points from content (simple extraction)"""
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        return sentences[:max_points]
