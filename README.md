## Django Restful 项目模板

欢迎使用 Django Restful 项目模板！本模板为使用 Django 框架构建强大且可扩展的 RESTful API 提供了稳固的基础。无论您是要启动新项目还是增强现有项目，本模板都提供了结构化的设置，秉持最佳实践原则。

主要特点：

预设设置，帮助您创建基于 Django 的 RESTful API
集成认证和授权机制
结构化的项目布局，有助于更好地组织代码
与热门第三方包的集成
详细的文档和使用示例
使用本模板，您可以快速开始开发下一个 Django RESTful API 项目。专注于业务逻辑和应用功能，模板将负责基础设置。使用 Django Restful 项目模板创建安全、高效且易于维护的 API。

## 🚀 快速开始

初始化项目

```
# 创建项目文件夹

mkdir hello-world
cd hello-world

# 克隆仓库
git clone https://github.com/zmaplex/django-restful-project-template.git .

sudo bash tools.sh init

source venv/bin/activate
```

新建 app
```
python manage.py startapp helloworld
```
打开 conf/urls 文件
```python
# ...
from common.apis import user
# ...
# 添加此行
from helloworld.apis import main as helloworld

router = DefaultRouter()
router.register(r"user", user.UserView)

# ...
# 添加此行
router.register(r"helloworld", helloworld.MainView)

# ...
``` 

运行

```bash
bash run.sh
```
访问 api 

```bash
curl http://127.0.0.1:8000/api/helloworld/ping/
```

将会看见 
```json
{
    "message": "pong"
}
```
