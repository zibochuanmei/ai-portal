# 本地开发与 Git 上传步骤

## 一、项目目录

当前项目目录：

    D:\ai\ai-portal

项目已从临时 worktree 迁移到上述日常开发目录，后续开发和 Git 操作都在该目录进行。不要把外层目录中的历史文档和其他项目一起上传。

## 二、本地首次启动

开始前确认四台电脑统一使用 Python 3.13.15、Node.js 24.21.0 和 Git for Windows 2.55.0.5。执行 `scripts/verify-environment.ps1` 会按命令行可识别的 2.55.0 或更高版本检查；Windows Git 的安装包构建号不要求与命令行输出完全一致。

在 ai-portal 目录打开 PowerShell。

### 1. 准备环境变量

    Copy-Item infra/.env.example infra/.env

开发环境可以先使用模板中的默认值；正式服务器必须更换数据库和 MinIO 密码。

### 2. 启动基础服务

确保 Docker Desktop 已启动，然后执行：

    docker compose --env-file infra/.env -f infra/docker-compose.yml up -d

查看容器：

    docker compose --env-file infra/.env -f infra/docker-compose.yml ps

### 3. 启动后端

打开新的 PowerShell：

    cd backend
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -e .
    uvicorn app.main:app --reload --port 8000

验证：

    http://localhost:8000/health

返回 status 为 ok 才表示后端启动成功。

后端日志会同时输出到当前终端和 `logs/backend/ai-portal.jsonl`。如果接口出现异常，先复制响应头中的 `X-Request-ID`，再按 `docs/日志与调试说明.md` 查询完整请求链路。

### 4. 启动前端

再打开一个新的 PowerShell：

    cd frontend
    npm install
    npm run dev

浏览器访问：

    http://localhost:5173

## 三、首次上传 Git

建议在 GitHub 或公司 Git 服务上新建一个空仓库，仓库名称使用 ai-portal，不要先自动创建 README。

在 ai-portal 目录执行：

    git init
    git add .
    git commit -m "chore: initialize ai portal project skeleton"
    git branch -M main
    git remote add origin <远程仓库地址>
    git push -u origin main

团队协作分支：

    git switch -c develop
    git push -u origin develop

以后开发功能时，从 develop 创建个人分支，例如：

    git switch develop
    git pull
    git switch -c feature/database-auth

## 四、上传前检查

    docker compose --env-file infra/.env.example -f infra/docker-compose.yml config --quiet
    python -m compileall -q backend/app
    git status

确认以下内容没有被上传：

- infra/.env
- backend/.venv
- frontend/node_modules
- API Key、数据库密码和服务器私钥

这些内容已经在 ai-portal/.gitignore 中配置为忽略。
