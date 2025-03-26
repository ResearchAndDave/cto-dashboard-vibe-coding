from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.api import dashboard
from app.database import init_db, seed_demo_data
from app.config import settings

# Initialize templates with custom functions
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
templates.env.globals.update({
    "min": min,
    "max": max,
    "progress_percent": 0  # Add a default value for progress_percent
})
# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Dashboard for technical leadership to monitor project metrics",
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

# Include API routers
app.include_router(dashboard.router, tags=["dashboard"])


@app.on_event("startup")
async def startup_event():
    """Initialize database and seed demo data on startup."""
    init_db()
    seed_demo_data()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
