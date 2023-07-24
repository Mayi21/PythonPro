import os
import subprocess

from fastapi import UploadFile, File
from fastapi import FastAPI, Request
from fastapi_limiter import FastAPILimiter
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from constant import InstanceEnv
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



# 应用限流策略到接口
@app.get("/limited_endpoint/")
@limiter.limit("5/minute")
async def limited_endpoint(request: Request):
    return {"message": "This endpoint is limited per second."}

class Cmd(BaseModel):
    name: str
    description: str
    value: str

# health api
@app.get("/health")
async def get_info():
    return {"status": 200}

@app.post("/cmd")
async def run_cmd(command: Cmd):
    return __exec_cmd(command.value)

# use to execute local shell file in /opt/plugin
@app.get("/exec-shell")
async def execute_shell_file(file_name: str):
    shell_file_path = os.path.join(InstanceEnv.PLUGIN_SCRIPT_PATH.value, file_name)
    return __exec_cmd('sh ' + shell_file_path)

@app.post('/uploadfiles')
async def upload_shell_file(file: UploadFile=File(...)):
    # need a front page that
    # 1.must end with .sh (optional)
    # 2.check size (must)
    # 3.rate limitation  (must)
    file_data = file.file.read()
    if file.size / 1024 >= 1024:
        return {'error': 'shell script to large'}
    file_name = file.filename
    if not file_name.endswith(".sh"):
        return {'error': 'file check not match'}
    print(file_name)
    # 1.save to the specified folder
    # 2.consider duplicate file name
    # for transport with name and attr,save in local temp dir then send to des from local
    with open(file_name, 'wb') as f:
        f.write(file_data)


    return {"filename": file.filename}


# file upload test
@app.get("/")
async def main():
    content = """
<body>
    <form action="/uploadfiles" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit" value="Upload">
    </form>
</body>
    """
    return HTMLResponse(content=content)


def __exec_cmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print("output", output)
    print("error", error)
    return output.decode().strip()

if __name__ == '__main__':
    os.system('uvicorn agent_server:app --reload')

