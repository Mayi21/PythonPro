import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/{name}")
async def home(request: Request, name: str):

    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name
    })


if __name__ == '__main__':
    os.system('uvicorn test:app --reload')
