#############################################
# do not alter tests in this file
#############################################
import pytest
from fastapi.testclient import TestClient
from cc_simple_server.server import app
from cc_simple_server.database import init_db, get_db_connection

# init db
init_db()

# FastAPI test client
client = TestClient(app)


def clear_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    clear_db()
    yield
    clear_db()


# Test the root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Cloud Computing!"}


def test_create_task():
    payload = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]


def test_get_tasks():
    client.post("/tasks/", json={"title": "Task 1", "description": "First task", "completed": False})
    client.post("/tasks/", json={"title": "Task 2", "description": "Second task", "completed": True})

    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 1"
    assert tasks[1]["title"] == "Task 2"


def test_update_task():
    create_response = client.post("/tasks/", json={"title": "Initial Task", "description": "Initial description", "completed": False})
    task_id = create_response.json()["id"]

    update_payload = {
        "title": "Updated Task",
        "description": "Updated description",
        "completed": True
    }
    update_response = client.put(f"/tasks/{task_id}/", json=update_payload)
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == update_payload["title"]
    assert updated_task["description"] == update_payload["description"]
    assert updated_task["completed"] == update_payload["completed"]


def test_delete_task():
    create_response = client.post("/tasks/", json={"title": "Task to Delete", "description": "To be deleted", "completed": False})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}/")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Task {task_id} deleted successfully"}
