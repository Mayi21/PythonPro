# 使用 Python 3.9 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 安装项目依赖包
RUN pip install -r requirements.txt

# 运行 Python 脚本
CMD ["python", "app.py"]
