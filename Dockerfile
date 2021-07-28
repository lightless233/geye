FROM python:3-buster
EXPOSE 8000

# 设置工作目录
WORKDIR /app

# 声明容器中的 /app 是匿名卷
VOLUME /app

# 复制代码到 docker 中
ADD . /app/

# 安装 nodejs
RUN sed -i 's#http://deb.debian.org#https://mirrors.aliyun.com#g' /etc/apt/sources.list && \
    apt update && \
    curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt install -y nodejs

# 构建前端代码
RUN ls /app/ && cd /app/geye-fe/ && npm i --registry https://registry.npm.taobao.org \
    && npm run build

# 安装Python的相关依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install "requests[socks]" "gunicorn[tornado]" -i https://pypi.tuna.tsinghua.edu.cn/simple

# 初始化DB
RUN python manage.py migrate

ENV PYTHONUNBUFFERED=1

CMD cd /app/ && bash start_geye_in_docker.sh
