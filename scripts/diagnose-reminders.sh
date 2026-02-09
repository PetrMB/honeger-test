#!/bin/bash
# Check Reminders permission status and provide guidance

echo "🔍 Diagnosing Apple Reminders Access..."
echo ""

# Test osascript access
echo "1️⃣ Testing osascript access..."
result=$(osascript -e 'tell application "Reminders" to name of lists' 2>&1)
if [ $? -eq 0 ]; then
    echo "   ✅ osascript works!"
    echo "   Lists: $result"
else
    echo "   ❌ osascript failed: $result"
fi
echo ""

# Test remindctl
echo "2️⃣ Testing remindctl access..."
if command -v remindctl &> /dev/null; then
    result=$(remindctl status 2>&1)
    if [ $? -eq 0 ]; then
        echo "   ✅ remindctl available"
        echo "   Status: $result"
    else
        echo "   ⚠️ remindctl error: $result"
    fi
else
    echo "   ⚠️ remindctl not installed"
    echo "   Install with: brew install steipete/tap/remindctl"
fi
echo ""

# Check if Terminal/iTerm has Reminders permission
echo "3️⃣ Checking permission status..."
echo "   System Settings → Privacy & Security → Reminders"
echo ""
echo "   Required fix:"
echo "   1. Open: open 'x-apple.systempreferences:com.apple.preference.security?Privacy_Reminders'"
echo "   2. Add Terminal.app or iTerm.app to the list"
echo "   3. Restart OpenClaw gateway: openclaw gateway restart"
echo ""
