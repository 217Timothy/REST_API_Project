#!/bin/sh

cd "$(dirname ($0)/..)"

echo "🚀 Upgrading database schema..."
flask --app main db upgrade
echo "✅ Database schema upgrade finished!"