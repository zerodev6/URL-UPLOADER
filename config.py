import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram API credentials
    APP_ID = int(os.environ.get("APP_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
    
    # Database
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    
    # Logging
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))
    
    # Owner
    OWNER_ID = int(os.environ.get("OWNER_ID", ""))
    
    # Session for user bot (if needed)
    SESSION_STR = os.environ.get("SESSION_STR", "")
    
    # Download/Upload settings
    MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4 GB
    SPEED_LIMIT = 10 * 1024 * 1024  # 10 MB/s
    CHUNK_SIZE = 512 * 1024  # 512 KB chunks
    
    # Download directory
    DOWNLOAD_DIR = "downloads"
