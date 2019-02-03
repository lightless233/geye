# GEYE

> GEYE是一款面向企业级以及白帽子的"More Fastest" Github监控工具，目的是为了在短时间内（例如15分钟内）发现Github上泄露的敏感数据。
> 同时GEYE也提供了便捷的Web管理界面，您可以在Web端对监控到的信息进行快速审查，并进行打标处理。
> 开箱即用！🚀🚀🚀

# 特性
- 开箱即用
- 基于GitHub API进行信息收集，快于大部分产品
- 方便的管理界面，快速打标处理
- 强大的规则系统，满足各种复杂搜索、过滤规则

![searchResult](https://raw.githubusercontent.com/redstone-project/geye/develop/docs/img/geye.png)
![monitorResult](https://raw.githubusercontent.com/redstone-project/geye/develop/docs/img/geye-monitor-results.png)

# 安装及快速开始
### 1. 部署需求
- Python 3.6.0 及以上版本
- Nginx
- PostgreSQL (未来会支持更多数据库)

### 2. 安装 & 部署

#### 2.1 安装环境
这里假设您已经有了Python3.6.0及以上版本，这里我们强烈推荐您使用virtualenv或pipenv创建虚拟环境，这样可以避免各种奇怪的问题。
如果您不想使用虚拟环境管理，也可以直接安装。但是下面的安装方法会基于存在virtualenv的情况下进行说明的。

```bash
$ git clone https://github.com/redstone-project/geye.git geye
$ cd geye
$ virtualenv -p python3 venv # 这里您可能需要指定您的python3.6.0及以上的解释器
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ pip install "requests[socks]"
$ pip install "gunicorn[tornado]"
```

#### 2.2 部署Web后端
在正式部署后端前，需要您手动复制几个内置的配置文件，并填入一些信息。

```bash
# 如果用于生产环境，请将dev.py修改为prod.py，预发环境请使用pre.py
# 并同时设置对应的环境变量GEYE_ENV，例如生产环境：
# export GEYE_ENV="prod"
# 如果不设置，默认为dev环境启动
(venv) $ cp ./geye/config/example.py ./geye/config/dev.py 
# ！！！1. 修改文件中的DEBUG开关以及SECRET_KEY！！！
# ！！！2. 配置pgsql的相关内容！！！
# ！！！3. 配置ALLOWED_CORS 和 ALLOWED_HOSTS！！！
# ！！！4. 其他配置项请酌情修改！！！
(venv) $ cp ./conf/gunicorn_config.example.py ./conf/gunicorn_conf.py
# ！！！1. 修改配置文件中的DEBUG开关！！！
# ！！！2. 其他配置项请酌情修改！！！
(venv) $ python manage.py migrate
(venv) $ chmod +x ./tools/*.sh && ./tools/start_web.sh

```

#### 2.3 部署Web前端
部署前端除了需要修改配置文件外，还需要配置nginx反向代理，这里提供了一份默认的nginx配置文件，只需要稍加修改即可。

```bash
$ cp ./geye-fe/src/config/index.example.js ./geye-fe/src/config/index.js
# ！！！修改你的域名！！！
$ cd geye-fe && npm run build && cd .. # 构建前端JS文件
$ cp ./APP-META/geye.nginx.conf /path/to/your/nginx/conf/dir/geye.nginx.conf
# ！！！1. 修改server_name！！！
# ！！！2. 修改root指向的路径，确保指向你刚刚clone的项目！！！
$ nginx -t && nginx -s reload
```

#### 2.4 部署引擎
```bash
(venv) $ python manage.py run --single 
```
#### 2.5 大功告成
Enjoy It!

# 版权信息
- GPL-3.0
