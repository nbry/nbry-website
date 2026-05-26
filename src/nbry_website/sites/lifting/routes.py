"""Route handlers for the lifting site."""

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from nbry_website.sites.lifting.lib.config_loader import ConfigLoader
from nbry_website.sites.lifting.lib.program_utils import (
    format_sets_display,
    get_display_name,
)

SITE_DIR = Path(__file__).parent
CONFIGS_DIR = SITE_DIR / "configs"
templates = Jinja2Templates(directory=str(SITE_DIR / "templates"))

router = APIRouter()


def _load_program(program_dir: str) -> dict[str, Any]:
    loader = ConfigLoader(CONFIGS_DIR / program_dir)
    exercises = ConfigLoader(CONFIGS_DIR).load("exercises.toml")
    program = loader.load("program.toml")["program"]
    for block in program["blocks"]:
        block_data = loader.load(block["file"])
        for day in block_data["days"]:
            for exercise in day["exercises"]:
                key = exercise["exercise"]
                exercise["name_display"] = get_display_name(key, exercises)
                exercise["sets_display"] = format_sets_display(exercise)
        block["data"] = block_data
    return program


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


@router.get("/program-guide", response_class=HTMLResponse)
async def program_guide(request: Request):
    """Instructions for running the program."""
    return templates.TemplateResponse(
        request=request, name="program-guide.html", context={"request": request}
    )


@router.get("/355-program", response_class=HTMLResponse)
async def program_355(request: Request):
    """355 program workout schedule."""
    program = _load_program("355-program")
    return templates.TemplateResponse(
        request=request,
        name="program.html",
        context={"request": request, "program": program},
    )


@router.get("/473-program", response_class=HTMLResponse)
async def program_473(request: Request):
    """473 program workout schedule."""
    program = _load_program("473-program")
    return templates.TemplateResponse(
        request=request,
        name="program.html",
        context={"request": request, "program": program},
    )


@router.get("/346-program", response_class=HTMLResponse)
async def program_346(request: Request):
    """346 program workout schedule."""
    program = _load_program("346-program")
    return templates.TemplateResponse(
        request=request,
        name="program.html",
        context={"request": request, "program": program},
    )


@router.get("/455-program", response_class=HTMLResponse)
async def program_455(request: Request):
    """455 program workout schedule."""
    program = _load_program("455-program")
    return templates.TemplateResponse(
        request=request,
        name="program.html",
        context={"request": request, "program": program},
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
