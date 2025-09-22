#!/bin/sh

cd "$(dirname "$0")/.."

echo "🔎 Generating new migration..."
flask --app main db migrate -m "${1:-auto migration}"

echo "📦 Applying migration..."
flask --app main db upgrade

echo "✅ Database schema is now up-to-date!"