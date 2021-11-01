FROM python:3-buster
EXPOSE 80

# 设置工作目录
WORKDIR /app

# 声明容器中的 /app 是匿名卷
# VOLUME /app

# 复制代码到 docker 中
ADD . /app/

# 安装 nodejs, nginx
RUN sed -i 's#http://deb.debian.org#https://mirrors.aliyun.com#g' /etc/apt/sources.list && \
    sed -i 's#security.debian.org/debian-security#mirrors.ustc.edu.cn/debian-security#g' /etc/apt/sources.list && \
    # curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    curl -sSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    echo "deb https://mirrors.ustc.edu.cn/nodesource/deb/node_14.x stretch main" >> /etc/apt/sources.list && \
    echo "deb-src https://mirrors.ustc.edu.cn/nodesource/deb/node_14.x stretch main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y apt-utils nodejs nginx && \
    apt-get autoremove -y

# 构建前端代码
RUN ls -alh /app/ && \
    cd /app/geye-fe/ && \
    npm i --registry https://registry.npm.taobao.org && \
    npm run build && \
    ls -alh /app/geye-fe/

# 安装Python的相关依赖
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ && \
    pip install "requests[socks]" "gunicorn[tornado]" -i https://mirrors.aliyun.com/pypi/simple/

RUN cp /app/conf/geye.nginx.conf /etc/nginx/conf.d/geye.conf

ENV PYTHONUNBUFFERED=1
CMD cd /app/ && sh docker_entrypoint.sh
