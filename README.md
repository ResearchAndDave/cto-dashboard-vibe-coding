# CTO Dashboard

A lightweight, accessible dashboard for CTOs and technical leadership to monitor project and product metrics.

## Tech Stack

- **Backend**: Python with FastAPI
- **Database**: DuckDB (local analytical database)
- **Frontend**: HTMX + DaisyUI + Tailwind CSS
- **Templating**: Jinja2

## Features

- Project overview with key technical metrics
- Status tracking and timeline visualization
- Team performance monitoring
- Sprint velocity tracking
- Technical debt and code quality metrics
- System health monitoring

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Node.js and npm (for Tailwind CSS compilation)

### Installation

1. Clone the repository (or unzip the project files)

```bash
git clone <repository-url>
cd cto-dashboard
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies

```bash
pip install -r requirements.txt
```

4. Install Node.js dependencies (for frontend build)

```bash
npm install
```

5. Build the CSS

```bash
npm run build:css
```

6. Initialize the database

```bash
python scripts/init_db.py
```

### Running the Application

Start the development server:

```bash
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload
```

The dashboard will be available at http://localhost:8000

## Development

### Watching for CSS changes

During development, you can automatically rebuild the CSS when files change:

```bash
npm run watch:css
```

### Running Tests

Run the test suite with pytest:

```bash
pytest
```

## Project Structure

```
cto-dashboard/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Configuration settings
│   ├── database.py            # DuckDB connection and setup
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   └── dashboard.py       # Dashboard data services
│   ├── api/                   # API routes
│   │   ├── __init__.py 
│   │   └── dashboard.py       # Dashboard API endpoints
│   ├── static/                # Static assets
│   │   ├── css/
│   │   │   ├── custom.css     # Custom CSS styles
│   │   │   └── output.css     # Compiled Tailwind CSS (generated)
│   │   └── js/
│   │       ├── htmx.min.js    # HTMX library
│   │       └── dashboard.js   # Dashboard-specific JavaScript
│   └── templates/             # Jinja2 templates
│       ├── base.html          # Base template with common structure
│       ├── dashboard.html     # Main dashboard page
│       └── components/        # Reusable UI components
│           ├── project_card.html
│           └── project_detail.html
├── scripts/                   # Utility scripts
│   └── init_db.py             # Database initialization script
├── src/                       # Frontend source files
│   └── css/
│       └── input.css          # Tailwind CSS source
├── tests/                     # Tests
│   ├── __init__.py
│   ├── test_api.py            # API tests
│   └── test_services.py       # Service tests
├── .env                       # Environment variables (not in version control)
├── package.json               # NPM configuration for frontend tools
├── tailwind.config.js         # Tailwind CSS configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Accessibility

This dashboard is designed to be WCAG AA compliant, featuring:

- Semantic HTML structure
- Proper labeling of interactive elements
- Color contrast meeting AA standards
- Keyboard navigation support
- Screen reader compatibility
- Focus management

## Data Model

The dashboard uses the following data model:

- **Projects**: Basic project information including name, description, status, timeline
- **Project Metrics**: Technical metrics such as code coverage, technical debt, system uptime
- **Sprint Velocity**: Sprint-by-sprint data showing planned vs. completed points

## API Endpoints

The dashboard provides the following API endpoints:

- `GET /api/projects`: List all projects
- `GET /api/projects/{id}`: Get a specific project
- `GET /api/projects/{id}/metrics`: Get metrics for a specific project
- `GET /api/projects/{id}/velocity`: Get velocity data for a specific project
- `GET /api/summary`: Get summary statistics for the dashboard

API documentation is available at `/api/docs` when running in debug mode.

## License

[MIT License](LICENSE)