#!/bin/bash
/opt/venv/bin/python health.py &
export LD_LIBRARY_PATH="$(dirname "$(find /nix/store -name "libmagic.so*" 2>/dev/null | head -1)"):$LD_LIBRARY_PATH"
export UPSTREAM_REPO="" MALLOC_ARENA_MAX=2
/opt/venv/bin/python update.py && exec /opt/venv/bin/python -m bot
