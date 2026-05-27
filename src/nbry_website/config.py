"""Shared configuration for all nbry sites."""

from enum import Enum

from pydantic import field_validator
from pydantic_settings import BaseSettings


class SiteMode(str, Enum):
    """Site operation mode."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class SiteSettings(BaseSettings):
    """Application settings from environment."""

    # Environment
    site_mode: SiteMode = SiteMode.DEVELOPMENT

    # Domains
    root_domain: str = "nbry.net"
    local_domain: str = "nbry.local"
    allowed_subdomains: list[str] = ["mycareer", "lifting", "coffee"]

    # Site toggles
    mycareer_site_enabled: bool = False
    lifting_site_enabled: bool = True
    coffee_site_enabled: bool = False

    @field_validator("allowed_subdomains", mode="before")
    @classmethod
    def parse_subdomains(cls, v: str | list[str]) -> list[str]:
        """Parse comma-separated string or list."""
        if isinstance(v, str):
            return [s.strip() for s in v.split(",")]
        return v

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
