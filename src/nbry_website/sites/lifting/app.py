"""Lifting site FastAPI application."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from nbry_website.sites.lifting import routes

# Create site-specific app
app = FastAPI(
    title="NBRY Lifting",
    description="Strength training program and resources",
)

# Site directory
SITE_DIR = Path(__file__).parent

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=str(SITE_DIR / "static")),
    name="static",
)

# Include routes
app.include_router(routes.router)


# Startup/shutdown events (if needed in future)
@app.on_event("startup")
async def startup_event():
    """Initialize lifting site resources."""
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup lifting site resources."""
    pass
