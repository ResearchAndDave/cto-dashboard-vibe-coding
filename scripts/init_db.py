#!/usr/bin/env python3
"""
Database initialization script.
This script can be run independently to set up the database.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the app
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import init_db, seed_demo_data


def main():
    """Initialize and seed the database."""
    print("Initializing database...")
    init_db()
    print("Database schema created successfully.")

    print("Seeding demo data...")
    seed_demo_data()
    print("Demo data seeded successfully.")

    print("Database setup complete!")


if __name__ == "__main__":
    main()
