"""Application configuration"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings from environment variables"""

    def __init__(self):
        # Database
        self.DATABASE_URL = os.getenv(
            'DATABASE_URL',
            'postgresql://postgres:postgres@localhost:5432/content_repurpose'
        )

        # JWT
        self.SECRET_KEY = os.getenv(
            'SECRET_KEY',
            'your-secret-key-change-this-in-production-min-32-chars-required'
        )
        self.ALGORITHM = 'HS256'
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.REFRESH_TOKEN_EXPIRE_DAYS = 7

        # Groq API
        self.GROQ_API_KEY = os.getenv(
            'GROQ_API_KEY',
            ''  # Set via GROQ_API_KEY environment variable
        )
        self.GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')

        # CORS
        self.ALLOWED_ORIGINS = [
            'http://localhost:3000',
            'http://localhost:3001',
            'http://127.0.0.1:3000',
        ]

        # File upload
        self.UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
        self.MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', str(50 * 1024 * 1024)))
        self.ALLOWED_FILE_EXTENSIONS = ['.txt', '.md', '.pdf', '.docx']

        # API
        self.API_PREFIX = '/api'
        self.DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

        # Create uploads directory if it doesn't exist
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)


settings = Settings()
