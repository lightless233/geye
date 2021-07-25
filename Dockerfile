FROM python:3-buster

ENV PYTHONUNBUFFERED=1

# 复制代码到 docker 中
WORKDIR /app
COPY . /app/

# 安装Python的相关依赖
RUN pip install -r requirements.txt

# 安装 nodejs
RUN sed -i 's#http://deb.debian.org#https://mirrors.aliyun.com#g' /etc/apt/sources.list && \
    apt update && \
    curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt install -y nodejs


