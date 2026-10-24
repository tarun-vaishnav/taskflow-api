# CRUD API tests


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn automated testing",
            "description": "Test TaskFlow with pytest",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] > 0
    assert data["title"] == "Learn automated testing"
    assert data["description"] == "Test TaskFlow with pytest"
    assert data["status"] == "pending"
    assert "created_at" in data
    assert "updated_at" in data



def test_list_tasks(client):
    client.post(
        "/tasks",
        json={
            "title": "Task One",
            "description": "First task",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "Task Two",
            "description": "Second task",
        },
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task One"
    assert data[1]["title"] == "Task Two"


def test_get_task_by_id(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Find this task",
            "description": "Testing retrieval by ID",
        },
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Find this task"


def test_get_nonexistent_task_returns_404(client):
    response = client.get("/tasks/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"



def test_patch_task_updates_only_provided_fields(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original title",
            "description": "Original description",
        },
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "in_progress"},
    )
    
    assert response.status_code == 200
    updated_task = response.json()

    assert updated_task["status"] == "in_progress"
    assert updated_task["title"] == "Original title"
    assert updated_task["description"] == "Original description"

    fetch_response = client.get(f"/tasks/{task_id}")
    assert fetch_response.json()["status"] == "in_progress"
    assert fetch_response.json()["title"] == "Original title"


def test_patch_empty_body_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Keep this task unchanged"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={})

    assert response.status_code == 422


def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Task to delete"},
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204

    fetch_response = client.get(f"/tasks/{task_id}")
    assert fetch_response.status_code == 404
