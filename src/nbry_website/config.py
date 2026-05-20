"""Shared configuration for all NBRY sites."""

from enum import Enum

from pydantic_settings import BaseSettings


class SiteMode(str, Enum):
    """Site operation mode."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class SiteSettings(BaseSettings):
    """Application settings from environment."""

    # Environment
    site_mode: SiteMode = SiteMode.DEVELOPMENT

    # Database
    database_url: str = "postgresql://postgres:postgres@postgres:5432/nbry_website"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # Domains
    root_domain: str = "nbry.com"
    local_domain: str = "nbry.local"
    allowed_subdomains: list[str] = ["career", "lifting", "coffee"]

    # Site toggles
    career_site_enabled: bool = False
    lifting_site_enabled: bool = True
    coffee_site_enabled: bool = False

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.site_mode == SiteMode.PRODUCTION

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.site_mode == SiteMode.DEVELOPMENT

    @property
    def base_domain(self) -> str:
        """Get base domain for current environment."""
        return self.root_domain if self.is_production else self.local_domain

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False
