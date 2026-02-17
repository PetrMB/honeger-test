#!/bin/bash

# Cloudflare Pages Deploy Script
# Automatizace deployed na Pages s GitHub source

set -e

echo "=== Cloudflare Pages Deploy ==="

# Nastavení proměnných
export CLOUDFLARE_ACCOUNT_ID=5470e26fcae9a4c79ec97311fd338cb4
export CLOUDFLARE_API_TOKEN="axoFp-kfDjlfatmhLXrZD4d1Z9ziN9WUzL35WF_b"

PROJECT_NAME=${1:-"otto"}
GITHUB_REPO=${2:-"PetrMB/otta-kanban"}
OUTPUT_DIR=${3:-"./"}

echo "Project: $PROJECT_NAME"
echo "GitHub: $GITHUB_REPO"
echo "Output dir: $OUTPUT_DIR"

# 1. Ověření API token
echo "👉 Ověřuji API token..."
curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.success'

# 2. Deployment
echo "👉 Deployuji přes Wrangler..."
cd "$OUTPUT_DIR"
wrangler pages deploy . --project-name="$PROJECT_NAME"

echo "✅ Deploy hotov!"
