# macOS Permission Types

Complete reference for macOS privacy permissions and their System Settings URLs.

## Common Permission Types

### Screen Recording

**What it allows:**
- Capture screen contents
- Record video of screen
- Take screenshots programmatically

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
```

**Typical users:**
- Screen recording tools (peekaboo, OBS)
- Screenshot utilities
- UI automation tools
- Remote desktop applications

**Testing:**
```bash
/usr/sbin/screencapture -x /tmp/test.png
```

---

### Accessibility

**What it allows:**
- Control other applications' UI
- Send keyboard/mouse events
- Read UI element properties
- Automate user interactions

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
```

**Typical users:**
- UI automation tools (peekaboo, AppleScript)
- Keyboard managers (Karabiner)
- Window managers (Rectangle)
- Macro tools

**Testing:**
```bash
osascript -e 'tell application "System Events" to get name of every process'
```

---

### Full Disk Access

**What it allows:**
- Read files in protected locations
- Access Mail, Messages, Safari data
- Read system logs
- Bypass standard file protections

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
```

**Typical users:**
- Backup tools (Time Machine)
- System cleaners
- File managers
- Development tools needing deep system access

**Protected locations:**
- `~/Library/Mail/`
- `~/Library/Messages/`
- `~/Library/Safari/`
- `/Library/Application Support/`

**Testing:**
```bash
ls ~/Library/Mail/
```

---

### Camera

**What it allows:**
- Access built-in or external cameras
- Capture photos and video

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Camera"
```

**Typical users:**
- Video conferencing (Zoom, Teams)
- Camera apps
- Media tools

---

### Microphone

**What it allows:**
- Access audio input devices
- Record audio

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone"
```

**Typical users:**
- Voice recorders
- Video conferencing
- Speech recognition

---

### Location Services

**What it allows:**
- Access device location
- Use GPS/Wi-Fi positioning

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_LocationServices"
```

**Typical users:**
- Maps applications
- Weather apps
- Location-based reminders

---

### Automation

**What it allows:**
- AppleScript control of specific apps
- Automate actions in other applications

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"
```

**Typical users:**
- AppleScript tools
- Workflow automation
- Cross-app integrations

**Note:** This is per-app automation. Example: "Terminal wants to control Finder"

---

### Input Monitoring

**What it allows:**
- Monitor keyboard input
- Observe mouse events
- Track system-wide input

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ListenEvent"
```

**Typical users:**
- Keyloggers (development/testing)
- Keyboard remappers
- Input event analyzers

---

### Files and Folders

**What it allows:**
- Access specific user folders
- Read/write to Documents, Downloads, Desktop

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_FilesAndFolders"
```

**Typical users:**
- File managers
- Editors
- Sync tools

**Note:** More granular than Full Disk Access

---

### Contacts

**What it allows:**
- Read contacts database
- Access address book

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Contacts"
```

---

### Calendars

**What it allows:**
- Read calendar events
- Create/modify events

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Calendars"
```

---

### Reminders

**What it allows:**
- Access reminders
- Create/modify reminder items

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Reminders"
```

---

### Photos

**What it allows:**
- Access Photos library
- Read/write photo metadata

**URL:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Photos"
```

---

## Quick Reference Table

| Permission | URL Parameter | Typical Use Case |
|-----------|--------------|------------------|
| Screen Recording | `Privacy_ScreenCapture` | Screenshots, screen recording |
| Accessibility | `Privacy_Accessibility` | UI automation, keyboard control |
| Full Disk Access | `Privacy_AllFiles` | System-wide file access |
| Camera | `Privacy_Camera` | Video capture |
| Microphone | `Privacy_Microphone` | Audio recording |
| Location | `Privacy_LocationServices` | GPS/location data |
| Automation | `Privacy_Automation` | Cross-app control |
| Input Monitoring | `Privacy_ListenEvent` | Keyboard/mouse tracking |
| Files & Folders | `Privacy_FilesAndFolders` | Specific folder access |
| Contacts | `Privacy_Contacts` | Address book |
| Calendars | `Privacy_Calendars` | Calendar events |
| Reminders | `Privacy_Reminders` | Reminder items |
| Photos | `Privacy_Photos` | Photos library |

## macOS Version Notes

- **macOS 13+:** Screen Recording and System Audio permissions split
- **macOS 14+:** Enhanced privacy controls, more granular permissions
- **URL schemes:** May change between major macOS releases

## Best Practices

1. **Request minimum necessary:** Only ask for permissions the tool actually needs
2. **Test after granting:** Always verify the permission works before proceeding
3. **Document requirements:** Note which permissions each tool requires
4. **Handle gracefully:** Check permissions before operations, provide clear error messages
5. **User education:** Explain why permissions are needed

## Programmatic Permission Checks

Most tools should implement their own permission checks:

```swift
// Swift example
import AVFoundation

AVCaptureDevice.authorizationStatus(for: .video)
// Returns: .authorized, .denied, .notDetermined, .restricted
```

```bash
# Bash approximation
if /usr/sbin/screencapture -x /tmp/test.png 2>&1 | grep -q "not allowed"; then
    echo "Screen Recording permission denied"
fi
```

## Resetting Permissions (for testing)

```bash
# Reset all permissions for an app (requires SIP disabled or Recovery mode)
tccutil reset All com.example.app

# Reset specific permission type
tccutil reset ScreenCapture com.example.app
tccutil reset Accessibility com.example.app
```

**Warning:** This requires special privileges and is mainly for development/testing.
