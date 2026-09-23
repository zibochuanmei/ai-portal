# API v1 初始约定

## GET /health

用于服务存活检查。

## GET /api/v1/me

返回当前登录用户及其部门、产品角色。

## GET /api/v1/workflows

返回当前用户有效授权后的工作流目录。Agent 是工作流内部的执行单元，权限不足的工作流不应出现在结果中。

## POST /api/v1/workflows/{workflow_id}/runs

请求：

{
  "conversation_id": "conv-demo-001",
  "file_ids": [],
  "inputs": {"message": "请整理这份会议纪要"}
}

响应至少包含：

- run_id
- workflow_id
- workflow_version_id
- status
- task_id
- answer
- citations

后续正式实现需要在服务端再次校验 agent_id，不能相信前端传入的 Agent 列表。
