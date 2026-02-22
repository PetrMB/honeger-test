#!/bin/bash
# Gateway watchdog – robustní verze (max 1 restart/hodinu)

set -euo pipefail

GATEWAY_PORT=18789
LOG_DIR="/Users/otto/.openclaw/workspace/logs"
LOG_FILE="$LOG_DIR/gateway-watchdog.log"
STATE_FILE="$LOG_DIR/gateway-watchdog.state"
MAX_RETRIES=3
RETRY_DELAY=600  # 10 minut mezi opakovanými pokusy
COOLDOWN_HOURS=1
WATCHDOG_ID="gateway-watchdog-v2"

mkdir -p "$LOG_DIR"

log() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
  echo "$msg" | tee -a "$LOG_FILE"
}

check_gateway() {
  if nc -z 127.0.0.1 "$GATEWAY_PORT" 2>/dev/null; then
    return 0
  else
    return 1
  fi
}

get_last_restart() {
  if [[ -f "$STATE_FILE" ]]; then
    cat "$STATE_FILE"
  else
    echo "0"
  fi
}

set_last_restart() {
  echo "$(date +%s)" > "$STATE_FILE"
}

should_restart() {
  local last_restart=$(get_last_restart)
  local now=$(date +%s)
  local diff=$((now - last_restart))
  local cooldown=$((COOLDOWN_HOURS * 3600))
  
  if [[ $diff -lt $cooldown ]]; then
    local remaining=$((cooldown - diff))
    log "⏸️  Cooldown: musíme počkat ještě $((remaining / 60)) minut"
    return 1
  fi
  return 0
}

restart_gateway() {
  log "🔄 Pokus $1/$MAX_RETRIES: restartuji gateway..."
  if openclaw gateway restart 2>&1; then
    sleep 2
    if check_gateway; then
      set_last_restart
      return 0
    fi
  fi
  return 1
}

# HLAVNÍ LOGIKA
log "🔍 Kontrola gateway (port $GATEWAY_PORT)..."

if check_gateway; then
  log "✅ Gateway OK"
  exit 0
fi

log "❌ Gateway DOWN!"

# Zkontrolovat cooldown (pokud už jsme restartovali v poslední hodině)
if ! should_restart; then
  log "⚠️  Cooldown aktivní – žádný další restart"
  exit 0
fi

log "🚀 Spouštím restartovací cyklus (max $MAX_RETRIES pokusů s 10min delay)..."

for attempt in $(seq 1 $MAX_RETRIES); do
  if restart_gateway "$attempt"; then
    log "✅ Gateway restartována úspěšně po $attempt. pokusu"
    exit 0
  fi
  
  if [[ $attempt -lt $MAX_RETRIES ]]; then
    log "⚠️  Restart neuspěšný ($attempt/$MAX_RETRIES), čekám $((RETRY_DELAY / 60)) minut..."
    sleep $RETRY_DELAY
  fi
done

# Pokud vše selhalo – Hack: launchctl kickstart
log "❌ Všechny $MAX_RETRIES restarty selhaly!"
log "⚡ Hack: launchctl kickstart"

if launchctl kickstart "gui/$UID/ai.openclaw.gateway" 2>/dev/null; then
  sleep 5
  if check_gateway; then
    log "✅ Hack úspěšný!"
    set_last_restart
    exit 0
  fi
fi

log "❌ I hack selhal. Potřeba manuální zásah."
exit 1
