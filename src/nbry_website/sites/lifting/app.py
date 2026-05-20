"""Lifting site FastAPI application."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from nbry_website.sites.lifting import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup: Initialize lifting site resources
    yield
    # Shutdown: Cleanup lifting site resources


# Create site-specific app
app = FastAPI(
    title="nbry Lifting",
    description="Strength training program and resources",
    lifespan=lifespan,
)

# Site directory
SITE_DIR = Path(__file__).parent

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=str(SITE_DIR / "static")),
    name="static",
)

# Mount shared static files
SHARED_DIR = SITE_DIR.parent.parent / "shared"
app.mount(
    "/shared",
    StaticFiles(directory=str(SHARED_DIR / "static")),
    name="shared",
)

# Include routes
app.include_router(routes.router)
