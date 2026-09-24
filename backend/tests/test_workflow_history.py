from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_owner_other_employee_and_admin_visibility() -> None:
    created = client.post(
        "/api/v1/workflows/document-assistant/runs",
        json={"inputs": {"message": "历史记录权限测试"}},
        headers={"X-Demo-User": "demo-employee-001"},
    )
    assert created.status_code == 202
    run_id = created.json()["run_id"]

    owner = client.get(
        f"/api/v1/workflow-runs/{run_id}",
        headers={"X-Demo-User": "demo-employee-001"},
    )
    other_employee = client.get(
        f"/api/v1/workflow-runs/{run_id}",
        headers={"X-Demo-User": "demo-employee-002"},
    )
    admin = client.get(
        f"/api/v1/workflow-runs/{run_id}",
        headers={"X-Demo-User": "demo-admin-001"},
    )

    assert owner.status_code == 200
    assert other_employee.status_code == 404
    assert other_employee.json()["error"]["code"] == "RUN_NOT_FOUND"
    assert admin.status_code == 200
