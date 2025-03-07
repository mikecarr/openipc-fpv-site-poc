#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f "/.env" ]; then
    source "/.env"
elif [ -f "/app/.env" ]; then
    source "/app/.env"
elif [ -f "../.env" ]; then
    source "../.env"
fi

# Allow command line arguments to override .env settings
DEVICE_IP=${1:-$DEVICE_IP}
DEVICE_USER=${2:-$DEVICE_USER}
DEVICE_PATH=${3:-$DEVICE_PATH}
LOCAL_PATH=${LOCAL_PATH:-"/app/"}
WATCH_INTERVAL=${WATCH_INTERVAL:-2}  # seconds

echo "Watching for changes and syncing to ${DEVICE_USER}@${DEVICE_IP}:${DEVICE_PATH}"
echo "Press Ctrl+C to stop"

# Ensure we have inotify-tools
apk add --no-cache inotify-tools

# Watch for file changes and sync when they occur
while true; do
    inotifywait -r -e modify,create,delete,move ${LOCAL_PATH}
    echo "Changes detected, syncing..."
    rsync -avz --delete ${LOCAL_PATH} ${DEVICE_USER}@${DEVICE_IP}:${DEVICE_PATH}
done