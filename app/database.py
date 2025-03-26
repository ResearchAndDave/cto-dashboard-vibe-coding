import duckdb
from app.config import settings
import os
from contextlib import contextmanager


def get_db_path():
    """Get the full path to the database file."""
    return os.path.join(settings.BASE_DIR, settings.DB_FILE)


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = duckdb.connect(get_db_path())
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize the database with required tables."""
    with get_connection() as conn:
        # Create projects table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                description VARCHAR,
                status VARCHAR NOT NULL,
                tech_stack VARCHAR,
                start_date DATE,
                target_end_date DATE,
                actual_end_date DATE,
                team_size INTEGER,
                team_composition VARCHAR,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create metrics table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS project_metrics (
                id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                metric_date DATE NOT NULL,
                sprint_completion_rate FLOAT,
                code_coverage FLOAT,
                technical_debt_ratio FLOAT,
                defect_escape_rate FLOAT,
                critical_bugs_count INTEGER,
                system_uptime FLOAT,
                avg_response_time FLOAT,
                error_rate FLOAT,
                team_capacity_utilization FLOAT,
                innovation_score FLOAT,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)

        # Create velocity table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sprint_velocity (
                id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                sprint_number INTEGER NOT NULL,
                planned_points FLOAT NOT NULL,
                completed_points FLOAT NOT NULL,
                sprint_start_date DATE,
                sprint_end_date DATE,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)


def seed_demo_data():
    """Seed the database with demo data."""
    with get_connection() as conn:
        # Check if data already exists
        result = conn.execute("SELECT COUNT(*) FROM projects").fetchone()
        if result[0] > 0:
            return  # Data already exists

        # Seed projects
        conn.execute("""
            INSERT INTO projects (id, name, description, status, tech_stack, start_date, target_end_date, team_size, team_composition)
            VALUES 
                (1, 'Customer Portal Redesign', 'Frontend modernization project', 'On Track', 'React, Node.js', '2023-10-01', '2024-06-30', 9, '7 Developers, 2 QA'),
                (2, 'Payment Gateway API', 'Backend infrastructure', 'At Risk', 'Java, Spring Boot, PostgreSQL', '2023-08-15', '2024-03-31', 6, '4 Developers, 1 QA, 1 DevOps'),
                (3, 'Data Lake Architecture', 'Cloud infrastructure', 'Delayed', 'AWS, Terraform, Python', '2023-11-01', '2024-05-31', 5, '3 Data Engineers, 2 Cloud Architects'),
                (4, 'Mobile App V2', 'Cross-platform mobile application', 'On Track', 'Flutter, Firebase', '2023-12-01', '2024-07-15', 7, '5 Developers, 2 QA')
        """)
        # Seed project metrics
        conn.execute("""
            INSERT INTO project_metrics (id, project_id, metric_date, sprint_completion_rate, code_coverage, technical_debt_ratio, defect_escape_rate, critical_bugs_count, system_uptime, avg_response_time, error_rate, team_capacity_utilization, innovation_score)
            VALUES 
                (1, 1, '2024-02-15', 92.5, 87.0, 12.0, 3.5, 2, 99.9, 45.0, 0.8, 85.5, 7.8),
                (2, 2, '2024-02-15', 78.3, 74.2, 18.5, 5.7, 4, 99.7, 120.0, 1.3, 90.2, 6.5),
                (3, 3, '2024-02-15', 65.2, 68.5, 22.7, 7.2, 5, 99.5, 230.0, 2.1, 95.7, 8.2),
                (4, 4, '2024-02-15', 88.7, 82.3, 9.5, 2.8, 1, 99.8, 75.0, 0.5, 82.3, 8.7)
        """)
        # Seed sprint velocity
        # Project 1 (Customer Portal)
        conn.execute("""
            INSERT INTO sprint_velocity (project_id, sprint_number, planned_points, completed_points, sprint_start_date, sprint_end_date)
            VALUES 
                (1, 1, 25, 23, '2023-10-01', '2023-10-14'),
                (1, 2, 30, 27, '2023-10-15', '2023-10-28'),
                (1, 3, 28, 30, '2023-10-29', '2023-11-11'),
                (1, 4, 32, 29, '2023-11-12', '2023-11-25')
        """)

        # Project 2 (Payment Gateway)
        conn.execute("""
            INSERT INTO sprint_velocity (project_id, sprint_number, planned_points, completed_points, sprint_start_date, sprint_end_date)
            VALUES 
                (2, 1, 20, 18, '2023-08-15', '2023-08-28'),
                (2, 2, 22, 19, '2023-08-29', '2023-09-11'),
                (2, 3, 25, 20, '2023-09-12', '2023-09-25'),
                (2, 4, 24, 18, '2023-09-26', '2023-10-09')
        """)

        # Project 3 (Data Lake)
        conn.execute("""
            INSERT INTO sprint_velocity (project_id, sprint_number, planned_points, completed_points, sprint_start_date, sprint_end_date)
            VALUES 
                (3, 1, 18, 15, '2023-11-01', '2023-11-14'),
                (3, 2, 20, 14, '2023-11-15', '2023-11-28'),
                (3, 3, 22, 13, '2023-11-29', '2023-12-12'),
                (3, 4, 20, 12, '2023-12-13', '2023-12-26')
        """)

        # Project 4 (Mobile App)
        conn.execute("""
            INSERT INTO sprint_velocity (project_id, sprint_number, planned_points, completed_points, sprint_start_date, sprint_end_date)
            VALUES 
                (4, 1, 24, 22, '2023-12-01', '2023-12-14'),
                (4, 2, 26, 25, '2023-12-15', '2023-12-28'),
                (4, 3, 28, 26, '2023-12-29', '2024-01-11'),
                (4, 4, 30, 27, '2024-01-12', '2024-01-25')
        """)
