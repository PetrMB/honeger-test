#!/bin/bash
# Wrapper for running sales check and returning results

LOG_FILE="/tmp/check-sales.log"

# Run the Python script
cd ~/.openclaw/workspace/scripts
python3 -u check-sales-improved.py > "$LOG_FILE" 2>&1

# Check if successful
if [ $? -eq 0 ]; then
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
