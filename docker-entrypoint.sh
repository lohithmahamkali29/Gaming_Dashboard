#!/bin/sh
set -e

echo "==> Applying Django migrations..."
python manage.py migrate --noinput

echo "==> Starting Sim Racing Control Center..."
exec python manage.py runserver 0.0.0.0:8000
