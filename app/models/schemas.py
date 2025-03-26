from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class ProjectBase(BaseModel):
    """Base model for project data."""

    name: str
    description: Optional[str] = None
    status: str
    tech_stack: Optional[str] = None
    start_date: Optional[date] = None
    target_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    team_size: Optional[int] = None
    team_composition: Optional[str] = None


class Project(ProjectBase):
    """Project model with ID and last updated timestamp."""

    id: int
    last_updated: Optional[datetime] = None


class ProjectMetrics(BaseModel):
    """Model for project metrics."""

    project_id: int
    metric_date: date
    sprint_completion_rate: Optional[float] = None
    code_coverage: Optional[float] = None
    technical_debt_ratio: Optional[float] = None
    defect_escape_rate: Optional[float] = None
    critical_bugs_count: Optional[int] = None
    system_uptime: Optional[float] = None
    avg_response_time: Optional[float] = None
    error_rate: Optional[float] = None
    team_capacity_utilization: Optional[float] = None
    innovation_score: Optional[float] = None


class SprintVelocity(BaseModel):
    """Model for sprint velocity data."""

    project_id: int
    sprint_number: int
    planned_points: float
    completed_points: float
    sprint_start_date: Optional[date] = None
    sprint_end_date: Optional[date] = None


class ProjectWithMetrics(Project):
    """Project model with associated metrics."""

    metrics: Optional[ProjectMetrics] = None
    velocity: Optional[List[SprintVelocity]] = None


class DashboardSummary(BaseModel):
    """Summary statistics for the dashboard."""

    total_projects: int
    on_track_count: int
    at_risk_count: int
    delayed_count: int
    avg_code_coverage: float
    avg_technical_debt: float
    critical_bugs_total: int
