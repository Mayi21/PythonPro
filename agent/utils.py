import os
import subprocess


def __exec_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        result = output.decode().strip() if output else error.decode().strip()
        return {"result": result}
    except Exception as e:
        return {"result": str(e)}

def check_shell_file(file_name):


    pass

def main():
    file_name = "test.sh"
    print(file_name.endswith(".sh"))
    os.system("ll")


if __name__ == '__main__':
    main()