#!/bin/bash
/opt/venv/bin/python health.py &
export UPSTREAM_REPO="" MALLOC_ARENA_MAX=2
/opt/venv/bin/python update.py && exec /opt/venv/bin/python -m bot
