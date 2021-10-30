# GEYE

> GEYE是一款面向企业级以及白帽子的"More Fastest" Github监控工具，目的是为了在短时间内（例如15分钟内）发现Github上泄露的敏感数据。
> 同时GEYE也提供了便捷的Web管理界面，您可以在Web端对监控到的信息进行快速审查，并进行打标处理。
> 开箱即用！🚀🚀🚀

# 0. 特性
- 设计说明：https://lightless.me/archives/How-To-Designing-A-Faster-Than-Faster-GitHub-Monitoring-System.html
- 开箱即用
- 基于GitHub API进行信息收集，快于大部分产品
- 方便的管理界面，快速打标处理
- 强大的规则系统，满足各种复杂搜索、过滤规则

![searchResult](https://raw.githubusercontent.com/redstone-project/geye/master/docs/img/geye.png)
![monitorResult](https://raw.githubusercontent.com/redstone-project/geye/master/docs/img/geye-monitor-results.png)

# 1. 快速开始

## 1.1 通过 docker 进行安装

### 拉取代码
```shell
git clone https://github.com/lightless233/geye.git geye
cd geye
```

### 修改配置
在使用 docker 进行部署前，需要对配置文件进行修改。首先将配置文件复制一份：
```shell
cp geye/settings/settings_example.py geye/settings/settings_prod.py
```

> 在 `docker-compose.yml` 文件中，有一个环境变量 `GEYE_ENV`，默认为 `prod`，表示生产环境。
> 
> 如果此值为 prod，则配置文件需要复制为 settings_prod.py
> 
> 如果将此值修改为 dev，则配置文件需要复制为 settings_dev.py

其中有几项设置需要进行修改：
- ALLOWED_HOSTS：
  - 允许访问的域名或IP，填写部署后实际使用的域名或IP，例如 `geye.lightless.me`，`192.168.62.100`;
- ALLOWED_CORS：
  - CORS 配置，通常和 ALLOWED_HOSTS 配置一样；
- USE_SEARCH_PROXY
  - 在抓去 Github 上的数据时，是否使用代理，True 使用代理，False 不使用代理；
- SEARCH_PROXIES
  - 如果 `USE_SEARCH_PROXY` 为 True，则该配置生效；
  - 目前仅支持 socks 代理，例如：`"http": "socks5://127.0.0.1:1080"`;
- REGEX_ENGINE
  - 指定使用何种引擎进行正则匹配，默认使用 Python 内置的 `re` 库；
  - Linux 环境推荐使用 `grep` 引擎；

其余配置项使用默认值即可，如有需要，也可手动进行调整；

### 启动
配置修改完成后，执行以下命令即可启动：
```shell
docker-compose up
```

## 1.2 手动安装

### 部署需求
- Python 3.6.0 及以上版本
- Nginx
- PostgreSQL (未来会支持更多数据库)

### 安装环境
这里假设您已经有了Python3.6.0及以上版本，这里我们强烈推荐您使用virtualenv或pipenv创建虚拟环境，这样可以避免各种奇怪的问题。
如果您不想使用虚拟环境管理，也可以直接安装。但是下面的安装方法会基于存在virtualenv的情况下进行说明的。

```bash
$ git clone https://github.com/lightless233/geye.git geye
$ cd geye
# 建议使用虚拟环境，不同版本的python可能创建虚拟环境的命令有所不同，请自行调整
$ virtualenv -p python3 venv 
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ pip install "requests[socks]"   # 可选，如果在抓取数据时不需要使用 socks5 代理，可以不安装。
$ pip install "gunicorn[tornado]" # 可选，根据 conf/gunicorn_config.py 中的 worker 类型决定。
```

### 部署Web后端
在正式部署后端前，需要您手动复制几个内置的配置文件，并填入一些信息。

```bash
# 如果用于开发测试环境，请将settings_example.py 复制为 settings_dev.py
# 并同时设置对应的环境变量GEYE_ENV="dev"
(venv) $ cp ./geye/settings/settings_example.py ./geye/settings/settings_prod.py
(venv) $ python manage.py migrate
(venv) $ export GEYE_ENV="prod" # 开发环境为 dev，如果不设置，默认为dev环境启动
(venv) $ chmod +x ./tools/*.sh && ./tools/start_web.sh
```

### 部署Web前端
部署前端除了需要修改配置文件外，还需要配置nginx反向代理，这里提供了一份默认的nginx配置文件，只需要稍加修改即可。

```bash
$ cd geye-fe && npm run build && cd .. # 构建前端JS文件
$ cp ./conf/geye.nginx.conf /path_to_your_nginx_conf_dir/geye.nginx.conf
$ vim /path_to_your_nginx_conf_dir/geye.nginx.conf # 修改 `root /app/geye-fe/dist/;` 指向刚刚前端 build 生成的 dist 目录
$ nginx -t && nginx -s reload
```

> 如果您更熟悉 caddy 等其他服务器，请自行配置。

### 启动引擎
引擎是监控 GitHub 的核心部分，目前仅支持 --single 模式启动，即`server`和`agent`一同启动，单机模式。

未来会支持单独启动 `--server` 和 `--agent` 模式，方便分布式部署，扩展应用。

```bash
(venv) $ python manage.py run --single 
```
