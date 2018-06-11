#!/usr/bin/env bash
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 5000 \
        -D \
        --reload \
        --access-logfile log/gunicorn-access.log \
        --error-logfile log/gunicorn-error.log \
        "app:create_app()"