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

echo "Syncing to ${DEVICE_USER}@${DEVICE_IP}:${DEVICE_PATH}"

# Use rsync to sync the app directory to the device
rsync -avz --delete ${LOCAL_PATH} ${DEVICE_USER}@${DEVICE_IP}:${DEVICE_PATH}

if [ $? -eq 0 ]; then
    echo "Sync completed successfully!"
else
    echo "Sync failed. Please check your connection and credentials."
fi