from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@app.get("/")
async def home(request: Request):
    """Home page of the website."""
    return templates.TemplateResponse(
        request=request, name="home.html", context={"request": request}
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
