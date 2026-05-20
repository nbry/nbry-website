"""Career site routes."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

SITE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(SITE_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Career site home page with full resume."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        },
    )
