# AI Portal

企业级多智能体 AI Portal 的 0 到 1 开发骨架。

当前阶段目标是跑通开发链路：Vue 前端、FastAPI 模块化单体后端、基础依赖服务，以及员工可见 Agent 的权限入口。复杂 Supervisor 编排、真实 SSO、RAG 入库和生产模型将在这个骨架上逐步实现。

## 目录

- frontend：Vue 3 + TypeScript + Vite 前端
- backend：FastAPI 后端
- infra：Docker Compose 和 Nginx 配置
- packages/contracts：前后端共享接口约定
- docs：项目设计和开发记录
- logs：本地和 Docker 运行日志（日志内容不提交 Git）

## 本地启动

1. 复制环境变量：
   Copy-Item infra/.env.example infra/.env

首次拉取项目后，先运行统一环境检查：

```powershell
.\scripts\verify-environment.ps1
```

四台开发电脑必须使用 Python 3.13.15、Node.js 24.21.0、Git for Windows 2.55.0.5（命令行按 2.55.0 或更高版本校验）、Docker Compose V2 和同一份 `infra/docker-compose.yml`。脚本会校验版本、Compose 项目名和配置展开结果；如果本机未安装 Docker，可临时使用 `-SkipDocker`，但启动服务前仍必须安装并启动 Docker Desktop。

环境变量说明和制衣业务适配见 `docs/环境配置与制造业适配说明.md`。参考依赖文件不能整份直接安装；当前先使用基础平台依赖，LangGraph、Torch、Embedding、Reranker 和本地模型在基础平台验收后分阶段加入。

本地 Compose 默认将数据库、Redis、MinIO、etcd 和 Milvus 数据写入项目根目录 `.data/`；部署到云服务器时，把 `DATA_ROOT` 改为 500 GB 数据盘目录，例如 `/data/ai-portal`。

2. 启动基础服务：
   docker compose --env-file infra/.env -f infra/docker-compose.yml up -d

3. 启动后端：
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -e .
   uvicorn app.main:app --reload --port 8000

4. 启动前端（新开一个终端）：
   cd frontend
   npm install
   npm run dev

打开 http://localhost:5173。后端健康检查地址为 http://localhost:8000/health。

后端默认同时输出控制台日志和 `logs/backend/ai-portal.jsonl`。每条请求日志都带有 `trace_id`，响应头中的 `X-Request-ID` 可以直接用于检索对应记录。Docker 启动后，后端日志位于 `logs/backend/`，Nginx 日志位于 `logs/nginx/`。具体排查方法见 `docs/日志与调试说明.md`。

## 第一版约定

- 当前使用演示身份 employee 和 platform_admin，尚未接企业 SSO。
- /api/v1/agents 返回后端根据用户权限计算出的可见 Agent，前端不自行判断权限。
- /api/v1/agent-runs 目前返回模拟结果，用于验证前后端链路；真实模型调用会接入 Model Gateway。
- Milvus 是唯一向量数据库；业务代码后续通过 VectorStoreService 访问，禁止直接散落连接。
- 当前日志已经按技术选型接入 `structlog + trace_id`；Prometheus/Grafana 和 Celery Worker 作为下一阶段基础设施接入，不在演示骨架中伪装成已完成能力。
- Compose 中 Milvus 和 etcd 只通过 Docker 内部网络访问，不映射宿主机端口；开发调试入口保留在前端、后端、PostgreSQL、Redis 和 MinIO。
