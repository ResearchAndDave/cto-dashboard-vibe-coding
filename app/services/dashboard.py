from app.database import get_connection
from app.models.schemas import Project, ProjectMetrics, SprintVelocity, DashboardSummary
from typing import List, Dict, Any, Optional
import pandas as pd


def get_all_projects() -> List[Project]:
    """Get all projects from the database."""
    with get_connection() as conn:
        query = "SELECT * FROM projects ORDER BY id"
        result = conn.execute(query).fetchall()

        # Convert to list of Project objects
        columns = [desc[0] for desc in conn.description]
        projects = []

        for row in result:
            project_dict = dict(zip(columns, row))
            projects.append(Project(**project_dict))

        return projects


def get_project_by_id(project_id: int) -> Optional[Project]:
    """Get a project by its ID."""
    with get_connection() as conn:
        query = "SELECT * FROM projects WHERE id = ?"
        result = conn.execute(query, [project_id]).fetchone()

        if result:
            columns = [desc[0] for desc in conn.description]
            project_dict = dict(zip(columns, result))
            return Project(**project_dict)

        return None


def get_project_metrics(project_id: int) -> Optional[ProjectMetrics]:
    """Get the latest metrics for a project."""
    with get_connection() as conn:
        query = """
            SELECT * FROM project_metrics 
            WHERE project_id = ? 
            ORDER BY metric_date DESC 
            LIMIT 1
        """
        result = conn.execute(query, [project_id]).fetchone()

        if result:
            columns = [desc[0] for desc in conn.description]
            metrics_dict = dict(zip(columns, result))
            return ProjectMetrics(**metrics_dict)

        return None


def get_project_velocity(project_id: int) -> List[SprintVelocity]:
    """Get sprint velocity data for a project."""
    with get_connection() as conn:
        query = """
            SELECT * FROM sprint_velocity 
            WHERE project_id = ? 
            ORDER BY sprint_number ASC
        """
        result = conn.execute(query, [project_id]).fetchall()

        # Convert to list of SprintVelocity objects
        columns = [desc[0] for desc in conn.description]
        velocity_data = []

        for row in result:
            velocity_dict = dict(zip(columns, row))
            velocity_data.append(SprintVelocity(**velocity_dict))

        return velocity_data


def get_dashboard_summary() -> DashboardSummary:
    """Get summary statistics for the dashboard."""
    with get_connection() as conn:
        # Project status counts
        total_query = "SELECT COUNT(*) FROM projects"
        on_track_query = "SELECT COUNT(*) FROM projects WHERE status = 'On Track'"
        at_risk_query = "SELECT COUNT(*) FROM projects WHERE status = 'At Risk'"
        delayed_query = "SELECT COUNT(*) FROM projects WHERE status = 'Delayed'"

        total_projects = conn.execute(total_query).fetchone()[0]
        on_track_count = conn.execute(on_track_query).fetchone()[0]
        at_risk_count = conn.execute(at_risk_query).fetchone()[0]
        delayed_count = conn.execute(delayed_query).fetchone()[0]

        # Metrics averages
        metrics_query = """
            SELECT 
                AVG(code_coverage) as avg_code_coverage,
                AVG(technical_debt_ratio) as avg_technical_debt,
                SUM(critical_bugs_count) as critical_bugs_total
            FROM project_metrics
            WHERE metric_date = (SELECT MAX(metric_date) FROM project_metrics)
        """
        metrics_result = conn.execute(metrics_query).fetchone()

        avg_code_coverage = metrics_result[0] or 0.0
        avg_technical_debt = metrics_result[1] or 0.0
        critical_bugs_total = metrics_result[2] or 0

        return DashboardSummary(
            total_projects=total_projects,
            on_track_count=on_track_count,
            at_risk_count=at_risk_count,
            delayed_count=delayed_count,
            avg_code_coverage=avg_code_coverage,
            avg_technical_debt=avg_technical_debt,
            critical_bugs_total=critical_bugs_total,
        )


def get_projects_with_metrics() -> List[Dict[str, Any]]:
    """Get all projects with their latest metrics."""
    projects = get_all_projects()
    result = []

    for project in projects:
        metrics = get_project_metrics(project.id)
        velocity = get_project_velocity(project.id)

        project_dict = project.model_dump()
        project_dict["metrics"] = metrics.model_dump() if metrics else None
        project_dict["velocity"] = (
            [v.model_dump() for v in velocity] if velocity else []
        )

        result.append(project_dict)

    return result
