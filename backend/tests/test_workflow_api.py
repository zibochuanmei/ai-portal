from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_workflow_catalog_returns_authorized_workflows() -> None:
    response = client.get("/api/v1/workflows")

    assert response.status_code == 200
    workflows = response.json()
    assert workflows
    assert {"workflow_id", "name", "can_run"}.issubset(workflows[0])


def test_workflow_run_uses_workflow_contract_and_returns_accepted() -> None:
    response = client.post(
        "/api/v1/workflows/document-assistant/runs",
        json={
            "conversation_id": "conv-demo-001",
            "file_ids": [],
            "inputs": {"message": "请整理这份会议纪要"},
        },
    )

    assert response.status_code == 202
    body = response.json()
    assert body["workflow_id"] == "document-assistant"
    assert body["status"] in {"queued", "running", "succeeded"}
    assert body["run_id"]


def test_workflow_run_survives_route_memory_reset() -> None:
    created = client.post(
        "/api/v1/workflows/document-assistant/runs",
        json={"inputs": {"message": "重启后仍可读取"}},
    )
    assert created.status_code == 202
    run_id = created.json()["run_id"]

    import app.api.routes as routes

    if hasattr(routes, "_runs"):
        routes._runs.clear()

    response = client.get(f"/api/v1/workflow-runs/{run_id}")
    assert response.status_code == 200
    assert response.json()["run_id"] == run_id


def test_workflow_run_is_visible_to_owner_but_not_another_employee() -> None:
    created = client.post(
        "/api/v1/workflows/document-assistant/runs",
        json={"inputs": {"message": "只允许本人读取"}},
    )
    run_id = created.json()["run_id"]

    owner_response = client.get(
        f"/api/v1/workflow-runs/{run_id}",
        headers={"X-Demo-User": "demo-employee-001"},
    )
    other_employee_response = client.get(
        f"/api/v1/workflow-runs/{run_id}",
        headers={"X-Demo-User": "demo-employee-002"},
    )

    assert owner_response.status_code == 200
    assert other_employee_response.status_code == 404
    assert other_employee_response.json()["error"]["code"] == "RUN_NOT_FOUND"


def test_unknown_workflow_returns_not_found() -> None:
    response = client.post(
        "/api/v1/workflows/not-authorized/runs",
        json={"inputs": {"message": "test"}},
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "WORKFLOW_NOT_FOUND"


def test_demo_admin_identity_is_available_for_route_guard_tests() -> None:
    response = client.get("/api/v1/me", headers={"X-Demo-User": "demo-admin-001"})

    assert response.status_code == 200
    assert response.json()["role"] == "platform_admin"


def test_file_upload_validates_extension_and_returns_owned_file() -> None:
    invalid = client.post(
        "/api/v1/files",
        files={"file": ("payload.exe", BytesIO(b"not allowed"), "application/octet-stream")},
    )
    assert invalid.status_code == 415
    assert invalid.json()["error"]["code"] == "FILE_TYPE_NOT_ALLOWED"

    valid = client.post(
        "/api/v1/files",
        files={"file": ("meeting.txt", BytesIO("会议纪要".encode("utf-8")), "text/plain")},
    )
    assert valid.status_code == 201
    body = valid.json()
    assert body["status"] == "uploaded"
    assert body["file_id"]
