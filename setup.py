# sync-forced-2025
from setuptools import setup, find_packages

setup(
    name="trebolsoft",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "pydantic-settings",
        "SQLAlchemy",
        "alembic",
        "psycopg2-binary",
        "python-dotenv",
    ],
)