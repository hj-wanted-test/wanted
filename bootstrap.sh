#!/bin/sh

echo "Starting.. WORKERS: $WORKERS, PORT: $PORT, ENV: $ENV"

gunicorn main:app --workers $WORKERS --bind 0.0.0.0:$PORT \
        --worker-class uvicorn.workers.UvicornWorker
