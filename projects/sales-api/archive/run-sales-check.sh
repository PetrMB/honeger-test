#!/bin/bash
# Wrapper for running sales check and returning results

LOG_FILE="/tmp/check-sales.log"
SCRIPT_DIR="$HOME/.openclaw/workspace/scripts"

# Cleanup old log
> "$LOG_FILE"

# Try v2 version first (uses remindctl), then fall back to original
if [ -f "$SCRIPT_DIR/check-sales-v2.py" ]; then
    cd "$SCRIPT_DIR"
    python3 -u check-sales-v2.py > "$LOG_FILE" 2>&1
    EXIT_CODE=$?
    
    # If v2 failed (likely permission issue), try original
    if [ $EXIT_CODE -ne 0 ]; then
        echo "⚠️ V2 script failed, trying original..." >> "$LOG_FILE"
        python3 -u check-sales-improved.py >> "$LOG_FILE" 2>&1
        EXIT_CODE=$?
    fi
else
    # Use original script
    cd "$SCRIPT_DIR"
    python3 -u check-sales-improved.py > "$LOG_FILE" 2>&1
    EXIT_CODE=$?
fi

# Check if successful
if [ $EXIT_CODE -eq 0 ]; then
    # Extract updated count from log
    UPDATED=$(grep -o "Updated [0-9]*" "$LOG_FILE" | grep -o "[0-9]*" | head -1)
    TOTAL=$(grep -o "Updated [0-9]*/[0-9]*" "$LOG_FILE" | grep -o "/[0-9]*" | grep -o "[0-9]*" | head -1)
    
    if [ -n "$UPDATED" ] && [ "$UPDATED" -gt 0 ]; then
        echo "✅ Kontrola letáků dokončena! Aktualizováno $UPDATED/$TOTAL položek v seznamu Nákupy."
        echo ""
        echo "📋 Podrobnosti najdeš v Apple Reminders - některé položky mají nové ceny a platnost akcí."
    else
        echo "✅ Kontrola letáků dokončena. Žádné nové akce pro tvoje položky."
    fi
else
    echo "❌ Chyba při kontrole letáků. Zkontroluj log: $LOG_FILE"
fi
