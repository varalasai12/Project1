import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
UPLOAD_DIR = BASE_DIR / "uploads"
MODEL_DIR = BASE_DIR / "models"

# Ensure directories exist
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

class Settings:
    SECRET_KEY: str = os.getenv("JWT_SECRET", "super-secret-classification-jwt-token-key-302910")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 day
    
    # Database
    DATABASE_URL: str = f"sqlite:///{INSTANCE_DIR}/app.db"
    
    # ML Model directory
    MODEL_DIR: Path = MODEL_DIR
    
    # Upload Settings
    UPLOAD_FOLDER: Path = UPLOAD_DIR
    ALLOWED_EXTENSIONS: set = {"txt", "pdf", "docx"}
    MAX_FILE_SIZE_MB: int = 10  # 10 MB limit

settings = Settings()
