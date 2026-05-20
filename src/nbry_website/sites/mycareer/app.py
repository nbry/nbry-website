"""Career site FastAPI application."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from nbry_website.sites.mycareer import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup: Initialize career site resources
    yield
    # Shutdown: Cleanup career site resources


# Create site-specific app
app = FastAPI(
    title="NBRY Career",
    description="Professional portfolio and resume",
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

# Templates
templates = Jinja2Templates(directory=str(SITE_DIR / "templates"))

# Include routes
app.include_router(routes.router)
