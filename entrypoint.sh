#!/bin/sh

cd /app

echo "⏳ Running database migrations..."
./scripts/upgrade.sh

echo "🚀 Starting Flask app..."
exec flask run --host=0.0.0.0 --debug