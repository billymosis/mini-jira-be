#!/bin/bash

# Run migrations
python manage.py migrate

# Start Gunicorn (with proper signal handling)
exec gunicorn config.asgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class uvicorn.workers.UvicornWorker \
    --graceful-timeout 5 \
    --timeout 10
