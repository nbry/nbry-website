"""Landing page for nbry.com."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from nbry_website.config import SiteSettings

app = FastAPI(title="NBRY")
site_settings = SiteSettings()

SITE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(SITE_DIR / "templates"))

# Mount static files
app.mount("/static", StaticFiles(directory=str(SITE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    """Main landing page with links to sub-sites."""
    scheme = request.url.scheme
    base_domain = site_settings.base_domain

    if base_domain == "localhost":
        lifting_url = f"{scheme}://localhost:8001"
        coffee_url = f"{scheme}://localhost:8002"
        mycareer_url = f"{scheme}://localhost:8003"
    else:
        lifting_url = f"{scheme}://lifting.{base_domain}"
        coffee_url = f"{scheme}://coffee.{base_domain}"
        mycareer_url = f"{scheme}://mycareer.{base_domain}"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "sites": [
                {
                    "name": "Career",
                    "url": mycareer_url,
                    "description": "My professional portfolio",
                    "icon": "💼",
                    "coming_soon": False,
                },
                {
                    "name": "Lifting",
                    "url": lifting_url,
                    "description": "The nbry powerbuilding program - training resources and guide",
                    "icon": "💪",
                },
                {
                    "name": "Coffee",
                    "url": coffee_url,
                    "description": "My coffee brewing diary and experiments",
                    "icon": "☕",
                    "coming_soon": True,
                },
            ],
        },
    )
