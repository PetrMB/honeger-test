#!/bin/bash
# deploy-otto-kanban.sh — Trigger Cloudflare Pages deployment
# Usage: ./deploy-otto-kanban.sh

set -e

# CREDENTIALS (vyplň Petr)
CLOUDFLARE_ACCOUNT_ID=""
CLOUDFLARE_API_TOKEN=""
PROJECT_NAME="otta-kanban"

# Source dir (github repo)
SOURCE_DIR="/tmp/otta-kanban"

if [ -z "$CLOUDFLARE_ACCOUNT_ID" ] || [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "❌ Chybí credentials!"
    echo ""
    echo "1. Získej ACCOUNT_ID:"
    echo "   https://dash.cloudflare.com/profile/api-tokens"
    echo ""
    echo "2. Vytvoř API token s právem: 'Cloudflare Pages — Edit'"
    echo "   URL: https://dash.cloudflare.com/profile/api-tokens"
    echo ""
    echo "3. Doplni do skriptu:"
    echo "   CLOUDFLARE_ACCOUNT_ID=..."
    echo "   CLOUDFLARE_API_TOKEN=..."
    exit 1
fi

# Build manifest (JSON soubor všech hashů)
MANIFEST=$(find "$SOURCE_DIR" -type f -exec shasum -a 256 {} \; | awk '{print "\"" $2 "\": \"" $1 "\""}' | paste -sd ',' | sed 's/^/{/;s/$/}/')

# Build commit info
COMMIT_HASH=$(git -C "$SOURCE_DIR" rev-parse HEAD 2>/dev/null || echo "manual-deploy-$(date +%s)")
COMMIT_MSG=$(git -C "$SOURCE_DIR" log -1 --pretty=%B 2>/dev/null || echo "manual update $(date)")

echo "🚀 Deploy to Cloudflare Pages"
echo "   Account: $CLOUDFLARE_ACCOUNT_ID"
echo "   Project: $PROJECT_NAME"
echo "   Commit:  $COMMIT_HASH"
echo ""

curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects/$PROJECT_NAME/deployments" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -F "branch=main" \
    -F "commit_dirty=false" \
    -F "commit_hash=$COMMIT_HASH" \
    -F "commit_message=$COMMIT_MSG" \
    -F "manifest=$MANIFEST" \
    -F "pages_build_output_dir=."

echo ""
echo "✅ Deploy triggered!"
