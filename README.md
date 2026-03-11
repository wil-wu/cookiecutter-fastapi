# Cookiecutter FastAPI 模板

基于 [Cookiecutter](https://cookiecutter.readthedocs.io/) 的 FastAPI 项目模板，用于快速生成带 Docker、uv 依赖管理与子服务结构的标准化 API 服务项目。

## 所用工具

模板生成的项目会用到以下工具与框架，便于事先了解：

- **[FastAPI](https://fastapi.tiangolo.com/)** — 现代、高性能的 Python Web 框架，基于 ASGI，内置 OpenAPI 文档、请求校验与异步支持。
- **[uv](https://docs.astral.sh/uv/)** — 由 Astral 开发的极速 Python 包管理与项目运行工具，兼容 pip/PyPI，用于依赖安装、锁定与执行脚本。
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI 服务器，常用于本地与生产环境运行 FastAPI 应用。
- **[Pydantic](https://docs.pydantic.dev/) / pydantic-settings** — 数据校验与配置管理，FastAPI 的请求体与配置多基于此。
- **[Docker](https://www.docker.com/)** — 容器化构建与运行，模板提供 Dockerfile 与 docker-compose，便于一致化部署。

## 前置要求

- [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html)（模板生成工具）
- [uv](https://docs.astral.sh/uv/)（项目管理工具）

## 快速开始

### 1. 使用模板生成项目

```bash
# 本地模板
cookiecutter /path/to/cookicutter-fastapi

# 远程仓库
cookiecutter gh:user/cookicutter-fastapi
```

按提示输入以下变量（或直接回车使用默认值）。

### 2. 模板变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `project_name` | 项目显示名称 | Vertu FastAPI template |
| `project_slug` | 项目目录名与包名（建议小写+连字符） | vertu-fastapi-template |
| `project_version` | 项目版本号 | 1.0.0 |
| `project_description` | 项目简介 | FastAPI project template for Vertu |
| `author` | 作者/团队 | Vertu |
| `python_version` | 所需 Python 版本 | 3.12 |
| `service_names` | 子服务名，逗号分隔（如 `service_a,service_b`） | service |
| `docker_repo` | Docker 镜像仓库前缀 | docker.vertu.com |

生成完成后，钩子会自动在项目目录内执行 `uv sync` 和 `git init`，并根据 `service_names` 在 `src/services/` 下创建对应子服务目录及标准文件。

### 3. 进入项目并运行

```bash
cd <project_slug>
uv run main.py
```

默认服务地址：`http://localhost:8000`（具体以 `src/config.py` 为准）。

## 生成的项目结构（示意）

```
<project_slug>/
├── src/
│   ├── __init__.py
│   ├── app.py              # 应用工厂
│   ├── config.py           # 全局配置（pydantic-settings）
│   ├── scanner.py          # 路由自动扫描注册
│   ├── core/               # 数据库、异常、中间件、共享（占位）
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   ├── middlewares.py
│   │   └── shared.py
│   └── services/           # 按 service_names 生成的子服务
│       └── <service_name>/
│           ├── config.py   # 子服务配置
│           ├── deps.py     # 依赖注入
│           ├── models.py   # 请求/响应模型
│           └── router.py   # 路由
├── tests/
├── main.py                 # 入口，uvicorn 启动
├── pyproject.toml          
├── Dockerfile
├── docker-compose.yml
├── docker-build.sh
├── .dockerignore
└── .gitignore
```

## Docker 使用

- **构建镜像**（可覆盖 `REPO`、`APP_NAME`、`VERSION`、`TIMESTAMP`）：
  ```bash
  ./docker-build.sh
  ```
- **编排运行**（需 `.env`，默认映射 8000、GPU、挂载源码）：
  ```bash
  docker compose up -d
  ```

## 开发与测试

- 安装/同步依赖：`uv sync`
- 运行测试：`uv run pytest`
- 代码检查/格式化：使用 `ruff`（见 `pyproject.toml` 的 dev 依赖）

## 许可证与维护

按项目需要添加许可证与维护说明。模板可用于各类 FastAPI 服务项目的标准化脚手架。
