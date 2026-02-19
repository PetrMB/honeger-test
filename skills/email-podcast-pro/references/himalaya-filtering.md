# Himalaya Email Filtering Reference

## Basic Commands

```bash
# List emails
himalaya list inbox --limit 10
himalaya list inbox --limit 100 --json

# Search emails
himalaya search --from "petr" --subject "důležité"
himalaya search --in "inbox" --after "2026-02-15"

# Read email
himalaya read <id>
himalaya read <id> --body
```

## Filtering Logic

### Word Count (minWords)
```bash
# Count words in email
himalaya read <id> --body | wc -w
```

### Paragraph Count
```bash
# Count paragraphs (empty lines)
himalaya read <id> --body | grep -c '^$'
```

### Spam Keywords
```bash
# Check for spam keywords
himalaya read <id> --body | grep -iqE "sleva|akce|kupón|předplatné|nabídka|speciální|výprodej"
```

### Spam Sender
```bash
# Check sender
himalaya list inbox --json | jq '.[].from[].address'
```

## Email Structure (JSON)

```json
{
  "id": "email-id",
  "subject": "Předmět emailu",
  "from": [
    {"name": "Jméno odesílatele", "address": "email@doména.cz"}
  ],
  "body": "Tělo emailu v HTML (musí se cleannout)",
  "received": "2026-02-19T10:00:00Z"
}
```

## Example Pipeline

```bash
# Get emails from last 3 days
himalaya list inbox --limit 100 --json | \
  jq -c --arg days "3" '[.[] | select(.received > (now - ($days |tonumber | . * 86400)))]'
```
