"""
Application configuration with environment-specific settings
"""
from enum import Enum
from typing import List
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Application environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application settings with dynamic environment configuration"""

    # Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "HackerHardware.net"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]

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

    def __init__(self, **kwargs):
        """Initialize settings with environment-specific defaults"""
        super().__init__(**kwargs)
        self._apply_environment_config()

    def _apply_environment_config(self):
        """Apply environment-specific configurations"""
        if self.ENVIRONMENT == Environment.DEVELOPMENT:
            self._configure_development()
        elif self.ENVIRONMENT == Environment.STAGING:
            self._configure_staging()
        elif self.ENVIRONMENT == Environment.PRODUCTION:
            self._configure_production()

    def _configure_development(self):
        """Development environment configuration"""
        self.LOG_LEVEL = "DEBUG"
        self.METRICS_ENABLED = True
        self.ENABLE_MTLS = False
        if not self.ALLOWED_ORIGINS:
            self.ALLOWED_ORIGINS = [
                "http://localhost:3000",
                "http://localhost:8000",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8000"
            ]

    def _configure_staging(self):
        """Staging environment configuration"""
        self.LOG_LEVEL = "INFO"
        self.METRICS_ENABLED = True
        self.ENABLE_MTLS = True
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 15
        if not self.ALLOWED_ORIGINS:
            self.ALLOWED_ORIGINS = [
                "https://staging.hackerhardware.net"
            ]

    def _configure_production(self):
        """Production environment configuration"""
        self.LOG_LEVEL = "WARNING"
        self.METRICS_ENABLED = True
        self.ENABLE_MTLS = True
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 15
        self.MAX_EDGE_NODES = 1000
        if not self.ALLOWED_ORIGINS:
            self.ALLOWED_ORIGINS = [
                "https://hackerhardware.net",
                "https://www.hackerhardware.net"
            ]

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == Environment.DEVELOPMENT

    @property
    def is_staging(self) -> bool:
        """Check if running in staging mode"""
        return self.ENVIRONMENT == Environment.STAGING

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == Environment.PRODUCTION


# Singleton instance
settings = Settings()
