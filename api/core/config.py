"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "HackerHardware.net"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Edge Nodes
    MAX_EDGE_NODES: int = 100
    NODE_HEARTBEAT_INTERVAL: int = 30
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Monitoring
    METRICS_ENABLED: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Zero-Trust
    ENABLE_MTLS: bool = True
    CERT_PATH: str = "/certs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
