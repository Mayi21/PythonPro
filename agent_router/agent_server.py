import subprocess

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cmd(BaseModel):
    name: str
    description: str
    value: str

@app.get("/health")
async def get_info():
    return {"status": 200}

@app.post("/cmd")
async def run_cmd(command: Cmd):
    return __exec_cmd(command.value)


def __exec_cmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print("output", output)
    print("error", error)
    return output.decode().strip()

