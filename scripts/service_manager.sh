#!/usr/bin/env bash

set -u

CONTAINER="${1:-}"
SERVICE="${2:-}"
ACTION="${3:-status}"

if [[ -z "$CONTAINER" || -z "$SERVICE" ]]; then
    echo "Usage: $0 <container> <service> <start|stop|restart|status>"
    exit 1
fi

case "$ACTION" in
    start|stop|restart|status) ;;
    *)
        echo "Invalid action: $ACTION"
        exit 1
        ;;
esac

if ! docker inspect "$CONTAINER" >/dev/null 2>&1; then
    echo "Error: Container not found."
    exit 1
fi

if [[ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER")" != "true" ]]; then
    echo "Error: Container is not running."
    exit 1
fi

docker exec "$CONTAINER" sh -c '
    service_name="$1"
    action="$2"

    if command -v service >/dev/null 2>&1; then
        exec service "$service_name" "$action"
    fi

    if command -v rc-service >/dev/null 2>&1; then
        exec rc-service "$service_name" "$action"
    fi

    if [ "$action" = "status" ]; then
        if ps -eo comm | grep -Fxq "$service_name"; then
            echo "$service_name process is running."
            exit 0
        fi

        echo "$service_name process is not running."
        exit 1
    fi

    echo "Service manager unavailable in this container."
    echo "Start/stop/restart requires a supported service manager."
    exit 127
' sh "$SERVICE" "$ACTION"

exit $?
