import os
import subprocess

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from starlette.responses import HTMLResponse

from constant import InstanceEnv

app = FastAPI()

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

