import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, seed_demo_data
import os


@pytest.fixture
def client():
    """Test client fixture."""
    # Use an in-memory database for testing
    os.environ["DB_FILE"] = ":memory:"

    # Initialize the test database
    init_db()
    seed_demo_data()

    # Create a TestClient for the FastAPI app
    with TestClient(app) as client:
        yield client


def test_get_projects(client):
    """Test the /api/projects endpoint."""
    response = client.get("/api/projects")
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)
    assert len(projects) > 0
    assert "name" in projects[0]
    assert "status" in projects[0]


def test_get_project_by_id(client):
    """Test the /api/projects/{id} endpoint."""
    # First, get a valid project ID
    projects_response = client.get("/api/projects")
    projects = projects_response.json()
    project_id = projects[0]["id"]

    # Then test getting that specific project
    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    project = response.json()
    assert project["id"] == project_id


def test_get_nonexistent_project(client):
    """Test getting a project that doesn't exist."""
    response = client.get("/api/projects/9999")
    assert response.status_code == 404


def test_get_project_metrics(client):
    """Test the /api/projects/{id}/metrics endpoint."""
    # First, get a valid project ID
    projects_response = client.get("/api/projects")
    projects = projects_response.json()
    project_id = projects[0]["id"]

    # Then test getting metrics for that project
    response = client.get(f"/api/projects/{project_id}/metrics")
    assert response.status_code == 200
    metrics = response.json()
    assert metrics["project_id"] == project_id
    assert "code_coverage" in metrics


def test_get_dashboard_summary(client):
    """Test the /api/summary endpoint."""
    response = client.get("/api/summary")
    assert response.status_code == 200
    summary = response.json()
    assert "total_projects" in summary
    assert "on_track_count" in summary
    assert "avg_code_coverage" in summary
