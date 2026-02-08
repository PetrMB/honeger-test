#!/bin/bash
# sync-ollama-models.sh - Synchronize Ollama models to OpenClaw config

set -e

OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
GATEWAY_URL="http://localhost:18789"
GATEWAY_TOKEN=$(jq -r '.gateway.auth.token' "$OPENCLAW_CONFIG")

echo "🔍 Zjišťuji Ollama modely..."
OLLAMA_MODELS=$(ollama list | tail -n +2 | awk '{print $1}' | grep -v "^$")

echo "📋 Dostupné Ollama modely:"
echo "$OLLAMA_MODELS" | nl

echo ""
echo "📝 Aktuální OpenClaw konfigurace:"
jq -r '.models.providers.ollama.models[]? | "  - \(.id) (\(.name))"' "$OPENCLAW_CONFIG"

echo ""
echo "🔄 Chceš synchronizovat všechny Ollama modely do OpenClaw? (y/n)"
read -r SYNC_ALL

if [[ "$SYNC_ALL" != "y" ]]; then
    echo "❌ Zrušeno"
    exit 0
fi

# Build JSON array of models
echo "🔨 Vytářím konfiguraci..."
MODELS_JSON="[]"

while IFS= read -r model; do
    # Skip cloud models (they're already configured differently)
    if [[ "$model" == *":cloud" ]]; then
        echo "  ⏭️  Přeskakuji cloud model: $model"
        continue
    fi
    
    # Extract base name and size
    MODEL_NAME=$(echo "$model" | sed 's/:/-/g' | sed 's/\b\(.\)/\u\1/g')
    
    # Determine context window based on model family
    CONTEXT=32768
    MAX_TOKENS=4096
    
    if [[ "$model" == llama3.2-vision* ]]; then
        CONTEXT=131072
        MODEL_NAME="Llama 3.2 Vision (Local)"
    elif [[ "$model" == qwen* ]]; then
        MODEL_NAME="Qwen $(echo $model | grep -oE '[0-9.]+' | head -1) (Local)"
    elif [[ "$model" == llama* ]]; then
        MODEL_NAME="Llama $(echo $model | grep -oE '[0-9.]+' | head -1) (Local)"
    fi
    
    MODEL_ENTRY=$(cat <<EOF
{
  "id": "$model",
  "name": "$MODEL_NAME",
  "reasoning": false,
  "input": ["text"],
  "cost": {
    "input": 0,
    "output": 0,
    "cacheRead": 0,
    "cacheWrite": 0
  },
  "contextWindow": $CONTEXT,
  "maxTokens": $MAX_TOKENS
}
EOF
)
    
    MODELS_JSON=$(echo "$MODELS_JSON" | jq --argjson entry "$MODEL_ENTRY" '. += [$entry]')
    echo "  ✅ Přidán: $model"
done <<< "$OLLAMA_MODELS"

# Add cloud models back
echo "  ℹ️  Přidávám cloud modely..."
CLOUD_MODELS=$(jq '.models.providers.ollama.models[]? | select(.id | endswith(":cloud"))' "$OPENCLAW_CONFIG")
if [[ -n "$CLOUD_MODELS" ]]; then
    MODELS_JSON=$(echo "$MODELS_JSON" | jq --argjson cloud "[$CLOUD_MODELS]" '. += $cloud')
fi

# Prepare config patch
CONFIG_PATCH=$(cat <<EOF
{
  "models": {
    "providers": {
      "ollama": {
        "models": $MODELS_JSON
      }
    }
  }
}
EOF
)

echo ""
echo "📤 Odesílám config patch na gateway..."

RESULT=$(curl -s -X POST "$GATEWAY_URL/api/gateway/config.patch" \
    -H "Authorization: Bearer $GATEWAY_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"raw\": $(echo "$CONFIG_PATCH" | jq -c | jq -R .),
        \"reason\": \"Sync Ollama models via sync-ollama-models.sh\"
    }")

if echo "$RESULT" | jq -e '.ok' > /dev/null 2>&1; then
    echo "✅ Konfigurace aktualizována!"
    echo ""
    echo "🔄 Gateway se restartuje..."
    echo "✨ Hotovo! Nové modely jsou k dispozici."
else
    echo "❌ Chyba při aktualizaci konfigurace:"
    echo "$RESULT" | jq .
    exit 1
fi
