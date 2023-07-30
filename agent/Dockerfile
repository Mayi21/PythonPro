# 使用 Python 3.9 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# install pip
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get update && apt-get install -y ca-certificates

RUN pip install --upgrade pip

RUN pip uninstall certifi
RUN pip install certifi

# 复制项目文件到容器中
COPY . /app

# 暴漏接口
EXPOSE 8000


# 安装项目依赖包
RUN pip install -r requirments.txt


# 运行 Python 脚本
CMD ["uvicorn", "agent_server:app", "--host", "0.0.0.0", "--port", "8000"]