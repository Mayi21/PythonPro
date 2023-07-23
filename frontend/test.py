import json
import os
import subprocess
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse("display.html", {
        "request": request,
    })

@app.post("/submit")
async def submit(request: Request, command: str=Form(...)):

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "res": output.decode()
    })
@app.post("/cmd")
async def cmd(cmd: str = Form(...)):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        result = output.decode().strip() if output else error.decode().strip()
        return {"result": result}
    except Exception as e:
        return {"result": str(e)}

@app.get('/search')
async def search(request: Request):
    return templates.TemplateResponse("search.html", {
        "request": request,
    })


from pydantic import BaseModel
import psutil
import time


class CPUUsage(BaseModel):
    time: str
    cpu_usage: float

@app.get("/get_cpu_usage/", response_model=CPUUsage)
async def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    current_time = datetime.now()

    # 将当前时间格式化为 'YYYY-MM-DD HH:mm' 格式的字符串
    time_format = '%M:%S'
    current_time = current_time.strftime(time_format)
    print(cpu_percent, current_time)
    return CPUUsage(time=current_time, cpu_usage=cpu_percent)


@app.get('/display-data')
def display_data(request: Request):
    return templates.TemplateResponse("display.html", {"request": request})

if __name__ == '__main__':
    # uvicorn.run("main:app  --reload", host="0.0.0.0", port=8000)
    os.system('uvicorn test:app --reload')




