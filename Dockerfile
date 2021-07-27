FROM python:3-buster
EXPOSE 8000

# 复制代码到 docker 中
WORKDIR /app
ADD . /app/

# 安装 nodejs
RUN sed -i 's#http://deb.debian.org#https://mirrors.aliyun.com#g' /etc/apt/sources.list && \
    apt update && \
    curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt install -y nodejs

# 构建前端代码
RUN cd /app/geye-fe/ && npm i --registry https://registry.npm.taobao.org \
    && npm run build

# 安装Python的相关依赖
RUN pip install -r requirements.txt && pip install "requests[socks]" "gunicorn[tornado]"

# 初始化DB
RUN python manage.py migrate

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["bash", "start_geye_in_docker.sh"]
