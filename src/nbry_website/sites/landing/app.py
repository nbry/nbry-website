"""Landing page for nbry.com."""
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="NBRY")

SITE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(SITE_DIR / "templates"))

# Mount static files
app.mount("/static", StaticFiles(directory=str(SITE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    """Main landing page with links to sub-sites."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "sites": [
                {
                    "name": "Lifting",
                    "url": "https://lifting.nbry.com",
                    "description": "Strength training program and resources",
                    "icon": "💪",
                },
                {
                    "name": "Coffee",
                    "url": "https://coffee.nbry.com",
                    "description": "Coffee brewing guides and reviews",
                    "icon": "☕",
                    "coming_soon": True,
                },
                {
                    "name": "Career",
                    "url": "https://career.nbry.com",
                    "description": "Professional portfolio and blog",
                    "icon": "💼",
                    "coming_soon": True,
                },
            ],
        },
    )
