"""Route handlers for the lifting site."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

SITE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(SITE_DIR / "templates"))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page of the website."""
    return templates.TemplateResponse(
        request=request, name="home.html", context={"request": request}
    )


@router.get("/philosophy", response_class=HTMLResponse)
async def philosophy(request: Request):
    """Program philosophy and training principles."""
    return templates.TemplateResponse(
        request=request, name="philosophy.html", context={"request": request}
    )


@router.get("/equipment", response_class=HTMLResponse)
async def equipment(request: Request):
    """Equipment requirements and recommendations."""
    return templates.TemplateResponse(
        request=request, name="equipment.html", context={"request": request}
    )


@router.get("/guide", response_class=HTMLResponse)
async def guide(request: Request):
    """Guide page of the website."""
    return templates.TemplateResponse(
        request=request, name="guide.html", context={"request": request}
    )


@router.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    """FAQ page of the website."""
    return templates.TemplateResponse(
        request=request, name="faq.html", context={"request": request}
    )


@router.get("/changelog", response_class=HTMLResponse)
async def changelog(request: Request):
    """Program changelog and version history."""
    return templates.TemplateResponse(
        request=request, name="changelog.html", context={"request": request}
    )


@router.get("/start", response_class=HTMLResponse)
async def getting_started(request: Request):
    """Links to external resources."""
    return templates.TemplateResponse(
        request=request, name="getting-started.html", context={"request": request}
    )


@router.get("/resources", response_class=HTMLResponse)
async def resources(request: Request):
    """Exercise form resources and videos."""
    return templates.TemplateResponse(
        request=request, name="resources.html", context={"request": request}
    )
