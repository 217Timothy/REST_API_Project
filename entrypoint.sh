#!/bin/sh

cd /app

echo "⏳ Running database migrations..."
./scripts/upgrade.sh

echo "🚀 Starting Flask app..."
exec gunicorn -b 0.0.0.0:80 --timeout 120 "main:create_app()"