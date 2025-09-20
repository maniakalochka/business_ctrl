#!/bin/sh
set -e

echo "Apply database migrations"
poetry run alembic upgrade head

echo "Starting gunicorn"
exec poetry run gunicorn -k uvicorn.workers.UvicornWorker src.app.main:app -b 0.0.0.0:8000