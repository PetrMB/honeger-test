---
name: macos-permissions
description: Grant macOS privacy permissions (Screen Recording, Accessibility, Full Disk Access, etc.) to CLI tools and applications. Use when a tool fails with permission errors or when you need to verify/grant system permissions for automation tools.
---

# macOS Permissions

Grant macOS privacy permissions to CLI tools and applications through System Settings automation.

## When to Use

- Tool fails with "permission denied" or "Screen Recording permission required"
- Need to verify current permission status
- Setting up new CLI tools that require system access
- Troubleshooting automation failures

## Common Permission Types

See [references/permission-types.md](references/permission-types.md) for details on all permission types and their URLs.

## Quick Workflow

### 1. Detect Missing Permission

Tools usually report missing permissions:
- Error messages: "Screen Recording permission is required"
- Dedicated check commands: `peekaboo permissions`, `tool --check-permissions`

### 2. Locate Binary

Find the exact binary path:

```bash
which <tool-name>
# Example: which peekaboo
# Output: /opt/homebrew/bin/peekaboo
```

Common locations:
- `/opt/homebrew/bin/*` (Homebrew on Apple Silicon)
- `/usr/local/bin/*` (Homebrew on Intel)
- `/Applications/*.app` (GUI applications)

### 3. Open System Settings

Use the appropriate URL scheme for the permission type:

```bash
# Screen Recording
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"

# Accessibility
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"

# Full Disk Access
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
```

See [references/permission-types.md](references/permission-types.md) for all permission URLs.

### 4. Add Binary via UI Automation

Use AppleScript to click the "+" button and add the binary:

```bash
osascript <<'EOF'
tell application "System Events"
    tell process "System Settings"
        set frontmost to true
        delay 0.5
        # Click the + button (adjust path based on permission type)
        click button 1 of group 1 of scroll area 1 of group 1 of group 2 of splitter group 1 of group 1 of window 1
    end tell
end tell
EOF
```

**Important:** The exact UI hierarchy changes between macOS versions. If this fails, use Accessibility Inspector to find the correct path.

### 5. Navigate to Binary

When the file picker opens:

```bash
osascript <<'EOF'
tell application "System Events"
    # Open "Go to Folder" dialog
    keystroke "g" using {command down, shift down}
    delay 0.5
    
    # Type the path
    keystroke "/opt/homebrew/bin"
    delay 0.3
    keystroke return
    
    # Type to search (optional if many files)
    delay 0.3
    keystroke "peekaboo"
    delay 0.5
    
    # Confirm selection
    keystroke return
end tell
EOF
```

### 6. Verify Permission

After adding, verify the tool can now access the permission:

```bash
# Tool-specific check
peekaboo permissions

# Or try the operation that failed before
peekaboo see --mode frontmost
```

## Full Example: Granting Screen Recording to Peekaboo

```bash
# 1. Detect issue
peekaboo permissions
# Output: Screen Recording (Required): Not Granted

# 2. Locate binary
which peekaboo
# Output: /opt/homebrew/bin/peekaboo

# 3. Open System Settings
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"

# 4-5. Add via UI automation
osascript <<'EOF'
tell application "System Events"
    tell process "System Settings"
        set frontmost to true
        delay 0.5
        
        # Click + button
        click button 1 of group 1 of scroll area 1 of group 1 of group 2 of splitter group 1 of group 1 of window 1
        delay 1
        
        # Navigate to binary
        keystroke "g" using {command down, shift down}
        delay 0.5
        keystroke "/opt/homebrew/bin"
        keystroke return
        delay 0.5
        
        # Select peekaboo
        keystroke "peekaboo"
        delay 0.5
        keystroke return
    end tell
end tell
EOF

# 6. Verify
peekaboo permissions
# Output: Screen Recording (Required): Granted
```

## Alternative: Using screencapture

If `peekaboo` or other tools fail, macOS's built-in `screencapture` can be used as fallback:

```bash
/usr/sbin/screencapture -x /tmp/screen.png
```

This works if the shell (Terminal/node/Clawdbot) already has Screen Recording permission.

## Troubleshooting

### UI Path Changed

If AppleScript fails with "can't get button X", the UI hierarchy changed:

1. Open `/System/Applications/Utilities/Accessibility Inspector.app`
2. Enable inspection mode (target icon)
3. Hover over the + button in System Settings
4. Note the exact path shown in Accessibility Inspector
5. Update the AppleScript accordingly

### Binary Not Found

If binary isn't in expected location:

```bash
# Search system-wide
mdfind -name "tool-name"

# Check if it's a shell function/alias
type tool-name

# For .app bundles
ls -la "/Applications/Tool Name.app/Contents/MacOS/"
```

### Permission Requires Restart

Some permissions (especially Accessibility) may require:
- Restarting the tool
- Restarting the Terminal
- Logging out and back in

### Already in List but Disabled

If the tool appears in the list but is toggled off:

```bash
osascript <<'EOF'
tell application "System Events"
    tell process "System Settings"
        # Find and click the toggle switch for the specific app
        # This requires knowing the exact row
    end tell
end tell
EOF
```

Or ask the user to manually enable it (simpler).

## Notes

- **Security:** macOS protects System Settings heavily. Some automation may require user interaction (clicking "OK" on prompts).
- **Versions:** UI paths and URLs change between macOS versions. This guide is tested on macOS 14+.
- **Accessibility Required:** UI automation itself requires Accessibility permission for Terminal/node/Clawdbot.
