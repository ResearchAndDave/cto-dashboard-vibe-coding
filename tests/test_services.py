"""
Tests for dashboard service functions.
"""

import pytest
import os
from app.services import dashboard
from app.database import init_db, seed_demo_data


@pytest.fixture(scope="module")
def setup_test_db():
    """Set up test database."""
    # Use an in-memory database for testing
    os.environ["DB_FILE"] = ":memory:"

    # Initialize the test database
    init_db()
    seed_demo_data()

    yield

    # No teardown needed for in-memory database


def test_get_all_projects(setup_test_db):
    """Test retrieving all projects."""
    projects = dashboard.get_all_projects()
    assert len(projects) > 0
    assert hasattr(projects[0], "id")
    assert hasattr(projects[0], "name")
    assert hasattr(projects[0], "status")


def test_get_project_by_id(setup_test_db):
    """Test retrieving a project by ID."""
    # Get first project to have a valid ID
    projects = dashboard.get_all_projects()
    first_project = projects[0]

    # Test retrieval by ID
    project = dashboard.get_project_by_id(first_project.id)
    assert project is not None
    assert project.id == first_project.id
    assert project.name == first_project.name


def test_get_nonexistent_project(setup_test_db):
    """Test retrieving a non-existent project."""
    project = dashboard.get_project_by_id(9999)
    assert project is None


def test_get_project_metrics(setup_test_db):
    """Test retrieving metrics for a project."""
    # Get first project to have a valid ID
    projects = dashboard.get_all_projects()
    first_project = projects[0]

    # Test metrics retrieval
    metrics = dashboard.get_project_metrics(first_project.id)
    assert metrics is not None
    assert metrics.project_id == first_project.id
    assert hasattr(metrics, "code_coverage")
    assert hasattr(metrics, "technical_debt_ratio")


def test_get_project_velocity(setup_test_db):
    """Test retrieving velocity data for a project."""
    # Get first project to have a valid ID
    projects = dashboard.get_all_projects()
    first_project = projects[0]

    # Test velocity data retrieval
    velocity = dashboard.get_project_velocity(first_project.id)
    assert len(velocity) > 0
    assert velocity[0].project_id == first_project.id
    assert hasattr(velocity[0], "sprint_number")
    assert hasattr(velocity[0], "planned_points")
    assert hasattr(velocity[0], "completed_points")


def test_get_dashboard_summary(setup_test_db):
    """Test retrieving dashboard summary."""
    summary = dashboard.get_dashboard_summary()
    assert hasattr(summary, "total_projects")
    assert hasattr(summary, "on_track_count")
    assert hasattr(summary, "at_risk_count")
    assert hasattr(summary, "delayed_count")
    assert hasattr(summary, "avg_code_coverage")
    assert hasattr(summary, "avg_technical_debt")
    assert hasattr(summary, "critical_bugs_total")


def test_get_projects_with_metrics(setup_test_db):
    """Test retrieving projects with their metrics."""
    projects_with_metrics = dashboard.get_projects_with_metrics()
    assert len(projects_with_metrics) > 0

    # Check the structure of the first project
    first_project = projects_with_metrics[0]
    assert "id" in first_project
    assert "name" in first_project
    assert "status" in first_project

    # Check that metrics and velocity are included
    assert "metrics" in first_project
    assert "velocity" in first_project
