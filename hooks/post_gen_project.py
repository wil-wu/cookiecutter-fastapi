#!/usr/bin/env python3
"""Post-generation hook: 初始化 uv 和 git 并创建子服务目录。"""
import os
import subprocess
import sys
from pathlib import Path

SERVICE_NAMES = "{{ cookiecutter.service_names }}"


def run(
    cmd: list[str],
    env: dict | None = None,
    check: bool = True,
    *,
    capture_output: bool = True,
) -> subprocess.CompletedProcess:
    env = env or os.environ.copy()
    return subprocess.run(
        cmd,
        cwd=Path.cwd(),
        env=env,
        check=check,
        capture_output=capture_output,
        text=True,
    )


def is_uv_available() -> bool:
    """检查系统是否已安装 uv。"""
    try:
        result = run(["uv", "--version"], check=False)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def is_git_available() -> bool:
    """检查系统是否已安装 git。"""
    try:
        result = run(["git", "--version"], check=False)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def init_git() -> None:
    """初始化 git 仓库，并将 gitignore 重命名为 .gitignore。"""
    if not is_git_available():
        return
    try:
        run(["git", "init"])
        print("Git repository initialized.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    gitignore_src = Path.cwd() / "gitignore"
    gitignore_dst = Path.cwd() / ".gitignore"
    gitignore_src.rename(gitignore_dst)


def sync_uv() -> None:
    """同步 uv 依赖（uv 为强依赖，未安装则退出）。"""
    if not is_uv_available():
        print("uv is required but not found. Install: https://docs.astral.sh/uv/", file=sys.stderr)
        sys.exit(1)
    try:
        run(["uv", "sync"], capture_output=False)
        print("uv dependencies synchronized.")
    except subprocess.CalledProcessError as e:
        msg = e.stderr or e.stdout or "uv sync failed."
        print("uv sync failed:", msg, file=sys.stderr)
        sys.exit(1)


def create_service_dirs() -> None:
    """
    按 service_names 为每个服务创建标准文件：__init__.py, config.py, deps.py, models.py, router.py
    """
    services_dir = Path.cwd() / "app" / "services"
    services_dir.mkdir(parents=True, exist_ok=True)
    names = [s.strip() for s in SERVICE_NAMES.split(",") if s.strip()]

    for name in names:
        svc_dir = services_dir / name
        svc_dir.mkdir(parents=True, exist_ok=True)
        prefix = name.replace("_", "-")
        files = {
            "__init__.py": "",
            "config.py": "# 子服务配置\n",
            "deps.py": "# 依赖注入\n",
            "models.py": "# 请求/响应模型（Pydantic）\n",
            "router.py": f'''from fastapi import APIRouter

router = APIRouter(prefix="/{prefix}", tags=["{name}"])
''',
        }
        for filename, content in files.items():
            (svc_dir / filename).write_text(content, encoding="utf-8")


def main() -> None:
    sync_uv()
    init_git()
    create_service_dirs()

    print("Project template generated successfully.")


if __name__ == "__main__":
    main()
