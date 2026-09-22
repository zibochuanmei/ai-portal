# API v1 初始约定

## GET /health

用于服务存活检查。

## GET /api/v1/me

返回当前登录用户及其部门、产品角色。

## GET /api/v1/agents

返回当前用户有效授权后的 Agent 列表。权限不足的 Agent 不应出现在结果中。

## POST /api/v1/agent-runs

请求：

{
  "agent_id": "document-assistant",
  "message": "请整理这份会议纪要",
  "file_ids": []
}

响应至少包含：

- run_id
- agent_id
- status
- answer
- citations

后续正式实现需要在服务端再次校验 agent_id，不能相信前端传入的 Agent 列表。
