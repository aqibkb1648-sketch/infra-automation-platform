#!/usr/bin/env bash

set -u

echo "===================================="
echo " Infrastructure Health Check"
echo "===================================="

check_command() {
    local name="$1"
    shift

    if "$@" >/dev/null 2>&1; then
        echo "[PASS] $name"
    else
        echo "[FAIL] $name"
    fi
}

check_command "Docker installed" docker --version
check_command "Docker daemon accessible" docker info
check_command "Containerlab installed" containerlab version

echo
echo "Running containers:"
docker ps --format "table {{.Names}}\t{{.Status}}"

echo
echo "Health check completed."
