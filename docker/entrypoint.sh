#!/bin/bash

set -e
set -u
set -o pipefail

log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') $@"
}

# Function to handle cleanup
cleanup() {
    log "Stopping processes..."
    kill -TERM "$PID_WSGI" "$PID_ASGI" 2>/dev/null || true
    log "Processes stopped."
}

trap cleanup SIGTERM SIGINT

log "Applying database migrations..."
python manage.py migrate --noinput || {
    log "Database migration failed!" >&2
    exit 1
}

if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_EMAIL:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
    log "Creating Django superuser..."
    if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists() or User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')"; then
        log "Failed to create superuser!" >&2
        exit 1
    else
        log "Superuser created or already exists."
    fi
else
    log "Skipping superuser creation as environment variables are not set."
fi

log "Starting Django WSGI server (runserver)..."
python manage.py runserver 0.0.0.0:8000 &
PID_WSGI=$!

log "Starting Django ASGI server (uvicorn)..."
uvicorn config.asgi:application --host 0.0.0.0 --port 8001 &
PID_ASGI=$!

# Wait for processes
pids=($PID_WSGI $PID_ASGI)

for pid in "${pids[@]}"; do
    if [[ $pid -ne 0 ]]; then
        wait "$pid" || {
            status=$?
            log "Process with PID $pid exited with status $status"
            exit $status
        }
    fi
done
