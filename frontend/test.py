import os

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse("index.html", {
        "request": request,
    })

@app.post("/submit")
async def submit(request: Request, command: str=Form(...)):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "cmd": command
    })

if __name__ == '__main__':
    os.system('uvicorn test:app --reload')
