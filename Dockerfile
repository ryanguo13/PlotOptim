FROM python:3.12-slim
LABEL authors="Ryan KWOK"
# 设置工作目录
WORKDIR /app

# 将当前目录中的内容复制到容器中的 /app 目录
COPY . /app

# 安装系统依赖项
RUN apt-get update && apt-get install -y \
    libegl1-mesa \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 设置 DISPLAY 环境变量以启用 GUI
ENV DISPLAY=:0

# 运行应用程序
CMD ["python", "main.py"]