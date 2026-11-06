#!/usr/bin/env bash

set -Eeuo pipefail

CONTAINER="${1:-}"
SOURCE_PATH="${2:-}"
BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

if [[ -z "$CONTAINER" || -z "$SOURCE_PATH" ]]; then
    echo "Usage: $0 <container_name> <container_path>"
    exit 1
fi

if [[ "$SOURCE_PATH" != /* ]]; then
    echo "Error: Container path must be absolute."
    exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
    echo "Error: Docker is not installed."
    exit 1
fi

if ! docker inspect "$CONTAINER" >/dev/null 2>&1; then
    echo "Error: Container not found: $CONTAINER"
    exit 1
fi

mkdir -p "$BACKUP_DIR"

DESTINATION="$BACKUP_DIR/${CONTAINER}-${TIMESTAMP}"

if ! docker cp "${CONTAINER}:${SOURCE_PATH}" "$DESTINATION"; then
    echo "Error: Backup failed."
    rm -rf "$DESTINATION"
    exit 1
fi

echo "[PASS] Backup created: $DESTINATION"
