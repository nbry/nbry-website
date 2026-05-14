from pathlib import Path
from fastapi import FastAPI

from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"request": request}
    )
