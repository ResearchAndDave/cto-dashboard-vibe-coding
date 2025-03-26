from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.services import dashboard
from app.models.schemas import Project, ProjectMetrics, SprintVelocity
from app.config import settings
from typing import List, Dict, Any
from pathlib import Path


router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


@router.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """Render the main dashboard page."""
    summary = dashboard.get_dashboard_summary()
    projects = dashboard.get_all_projects()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "summary": summary,
            "projects": projects,
            "title": settings.APP_NAME,
        },
    )


@router.get("/api/projects", response_model=List[Project])
async def get_projects():
    """API endpoint to get all projects."""
    return dashboard.get_all_projects()


@router.get("/api/projects/{project_id}", response_model=Project)
async def get_project(project_id: int):
    """API endpoint to get a specific project."""
    project = dashboard.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/api/projects/{project_id}/metrics", response_model=ProjectMetrics)
async def get_project_metrics(project_id: int):
    """API endpoint to get metrics for a specific project."""
    metrics = dashboard.get_project_metrics(project_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Project metrics not found")
    return metrics


@router.get("/api/projects/{project_id}/velocity", response_model=List[SprintVelocity])
async def get_project_velocity(project_id: int):
    """API endpoint to get velocity data for a specific project."""
    velocity = dashboard.get_project_velocity(project_id)
    if not velocity:
        raise HTTPException(status_code=404, detail="Project velocity data not found")
    return velocity


@router.get("/api/summary")
async def get_summary():
    """API endpoint to get dashboard summary statistics."""
    return dashboard.get_dashboard_summary()


@router.get("/components/project_card/{project_id}", response_class=HTMLResponse)
async def get_project_card(request: Request, project_id: int):
    """Endpoint to get a single project card for HTMX updates."""
    project = dashboard.get_project_by_id(project_id)
    metrics = dashboard.get_project_metrics(project_id)
    velocity = dashboard.get_project_velocity(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return templates.TemplateResponse(
        "components/project_card.html",
        {
            "request": request,
            "project": project,
            "metrics": metrics,
            "velocity": velocity,
        },
    )


@router.get("/components/project_detail/{project_id}", response_class=HTMLResponse)
async def get_project_detail(request: Request, project_id: int):
    """Endpoint to get detailed project information for HTMX modal."""
    project = dashboard.get_project_by_id(project_id)
    metrics = dashboard.get_project_metrics(project_id)
    velocity = dashboard.get_project_velocity(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return templates.TemplateResponse(
        "components/project_detail.html",
        {
            "request": request,
            "project": project,
            "metrics": metrics,
            "velocity": velocity,
        },
    )
