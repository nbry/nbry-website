from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).parent / "static")),
    name="static",
)


@app.get("/")
async def home(request: Request):
    """Home page of the website."""
    return templates.TemplateResponse(
        request=request, name="home.html", context={"request": request}
    )


@app.get("/philosophy")
async def philosophy(request: Request):
    """Program philosophy and training principles."""
    return templates.TemplateResponse(
        request=request, name="philosophy.html", context={"request": request}
    )


@app.get("/equipment")
async def equipment(request: Request):
    """Equipment requirements and recommendations."""
    return templates.TemplateResponse(
        request=request, name="equipment.html", context={"request": request}
    )


@app.get("/instructions")
async def instructions(request: Request):
    """Instructions page of the website."""
    return templates.TemplateResponse(
        request=request, name="instructions.html", context={"request": request}
    )


@app.get("/faq")
async def faq(request: Request):
    """FAQ page of the website."""
    return templates.TemplateResponse(
        request=request, name="faq.html", context={"request": request}
    )


@app.get("/changelog")
async def changelog(request: Request):
    """Program changelog and version history."""
    return templates.TemplateResponse(
        request=request, name="changelog.html", context={"request": request}
    )


@app.get("/links")
async def links(request: Request):
    """Links to external resources."""
    return templates.TemplateResponse(
        request=request, name="links.html", context={"request": request}
    )


@app.get("/resources")
async def resources(request: Request):
    """Exercise form resources and videos."""
    return templates.TemplateResponse(
        request=request, name="resources.html", context={"request": request}
    )
