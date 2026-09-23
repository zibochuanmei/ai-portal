# 本地开发与 Git 拉取和启动步骤

## 一、拉取项目

项目已经上传到 GitHub，组员不需要重新初始化仓库：

    cd D:\AI
    git clone https://github.com/zibochuanmei/ai-portal.git
    cd ai-portal
    git switch main

后续同步最新代码：

    git pull origin main

## 二、统一版本和环境变量

四台开发电脑统一使用：

- Python 3.13.15
- Node.js 24.21.0
- Git 2.55.0.5 或更高版本
- Docker Desktop 和 Compose V2（启动 PostgreSQL、Redis、MinIO、Milvus 时需要）

复制开发环境变量：

    Copy-Item infra/.env.example infra/.env

`infra/.env` 只用于本机开发，不能提交到 GitHub。正式服务器必须更换数据库、MinIO 和其他服务密码。

## 三、无 Docker 时先启动前后端演示

Docker 尚未安装时，可以先验证前端、后端、身份和工作流接口。此时数据库、Redis、MinIO 和 Milvus 还不会启动，文件只保存到本地开发目录。

打开第一个 PowerShell：

    cd D:\AI\ai-portal\backend
    py -3.13 --version
    py -3.13 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python --version
    python -m pip install -e ".[dev]"
    python -m uvicorn app.main:app --reload --port 8000

`py -3.13 --version` 和激活后的 `python --version` 都必须显示 Python 3.13.15。

打开第二个 PowerShell：

    cd D:\AI\ai-portal\frontend
    npm install
    npm run dev

浏览器访问 `http://localhost:5173`，后端健康检查为 `http://localhost:8000/health`。

## 四、Docker 安装后启动基础服务

安装并启动 Docker Desktop 后，在项目根目录执行：

    docker compose --env-file infra/.env -f infra/docker-compose.yml up -d
    docker compose --env-file infra/.env -f infra/docker-compose.yml ps

基础服务启动后，再按上面的步骤启动后端和前端。

## 五、团队分支协作

远程 `main` 保存可演示版本，功能开发从 `develop` 创建个人分支：

    git fetch origin
    git switch develop
    git pull origin develop
    git switch -c feature/database-auth

提交前至少执行：

    npm run build --prefix frontend
    git diff --check
    git status

## 六、上传前检查

不得提交以下内容：

- `infra/.env`
- `backend/.venv`
- `frontend/node_modules`
- API Key、数据库密码和服务器私钥
- `logs` 目录中的实际日志内容

这些内容已经在项目根目录 `.gitignore` 中配置为忽略。
