#!/bin/bash
# email-to-podcast.sh — Convert selected emails to podcast (Zuzana Premium)
# Usage: ./email-to-podcast.sh [--auto|--days N|--id <id>]

set -e

# Default config
CONFIG_DIR="${HOME}/.config/email-podcast-pro"
mkdir -p "$CONFIG_DIR"

# Config defaults
MIN_WORDS=500
EXCLUDE_KEYWORDS="sleva|akce|kupón|předplatné|nabídka|speciální|výprodej"
EXCLUDE_FROM="info@|newsletter@|noreply@|auto@"
OUTPUT_DIR="${HOME}/Music/Podcasts/Emaily"
VOICE="Zuzana"
RATE=150
FORMAT="mp3"

# Parse args
AUTO=false
DAYS=7
EMAIL_ID=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --auto)
            AUTO=true
            shift
            ;;
        --days)
            DAYS="$2"
            shift 2
            ;;
        --id)
            EMAIL_ID="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 [--auto|--days N|--id <id>]"
            exit 1
            ;;
    esac
done

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Load custom config if exists
if [ -f "$CONFIG_DIR/config.json" ]; then
    echo "🛠️  Loading custom config..."
    MIN_WORDS=$(jq -r '.filter.minWords // 500' "$CONFIG_DIR/config.json")
    EMAIL_ID="$(jq -r '.filter.emailId // ""' "$CONFIG_DIR/config.json")"
fi

# Function to clean HTML and extract plain text
clean_text() {
    echo "$1" | sed 's/<[^>]*>//g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | tr -s '\n' | tr -s ' '
}

# Function to count words
count_words() {
    echo "$1" | wc -w | tr -d ' '
}

# Function to count paragraphs
count_paragraphs() {
    echo "$1" | grep -c '^$' || echo 0
}

# Function to check for spam keywords
is_spam() {
    local text="$1"
    if echo "$text" | grep -iqE "$EXCLUDE_KEYWORDS"; then
        return 0
    fi
    return 1
}

# Function to check for spam sender
is_spam_sender() {
    local from="$1"
    if echo "$from" | grep -qiE "$EXCLUDE_FROM"; then
        return 0
    fi
    return 1
}

# Function to calculate URL density
url_density() {
    local text="$1"
    local url_count=$(echo "$text" | grep -oE 'https?://[^ ]+' | wc -l)
    local word_count=$(count_words "$text")
    if [ "$word_count" -eq 0 ]; then
        echo 0
        return
    fi
    echo "scale=2; $url_count * 100 / $word_count" | bc
}

# Function to generate podcast filename
generate_filename() {
    local subject="$1"
    local author="$2"
    local timestamp=$(date +%s)
    # Clean subject (remove special chars, limit length)
    local clean_subject=$(echo "$subject" | tr -cd '[:alnum:]_-' | cut -c1-50)
    echo "${OUTPUT_DIR}/podcast-${timestamp}-${clean_subject}.mp3"
}

echo "📩 Email-to-Podcast (Zuzana Premium)"
echo "====================================="
echo ""

# Get emails based on mode
if [ -n "$EMAIL_ID" ]; then
    echo "📄 Reading specific email: $EMAIL_ID"
    EMAILS_JSON=$(himalaya read "$EMAIL_ID" --raw 2>/dev/null)
else
    echo "📅 Getting emails from last $DAYS days..."
    EMAILS_JSON=$(himalaya list inbox --limit 100 --json 2>/dev/null | jq -c --arg days "$DAYS" '[.[] | select(.received > (now - ($days |tonumber | . * 86400)))]')
fi

# Process emails
PROCESSED=0
SKIPPED=0

echo ""
echo "🔄 Processing emails..."

# Parse emails
if [ -n "$EMAIL_ID" ]; then
    EMAIL_LIST=(1)
else
    EMAIL_COUNT=$(echo "$EMAILS_JSON" | jq 'length')
    echo "   Found $EMAIL_COUNT emails in last $DAYS days"
    EMAIL_LIST=$(echo "$EMAILS_JSON" | jq -c '.[]')
fi

echo "$EMAIL_LIST" | while read -r email; do
    if [ -z "$email" ]; then
        continue
    fi

    ID=$(echo "$email" | jq -r '.id // ""')
    SUBJECT=$(echo "$email" | jq -r '.subject // "Bez předmětu"')
    FROM=$(echo "$email" | jq -r '.from[].address // "unknown"')
    BODY=$(echo "$email" | jq -r '.body // ""')

    # Skip if no body
    if [ -z "$BODY" ] || [ "$BODY" == "null" ]; then
        echo "   ⏭️  Skipping $ID (no body)"
        continue
    fi

    # Clean body
    BODY=$(clean_text "$BODY")

    # Count stats
    WORDS=$(count_words "$BODY")
    PARAGRAPHS=$(count_paragraphs "$BODY")
    URL_DEN=$(url_density "$BODY")

    # Check filters
    SKIP_REASONS=""

    if [ "$WORDS" -lt "$MIN_WORDS" ]; then
        SKIP_REASONS="$SKIP_REASONS length($WORDS<$MIN_WORDS) "
    fi

    if is_spam "$BODY"; then
        SKIP_REASONS="$SKIP_REASONS spam_keywords "
    fi

    if is_spam_sender "$FROM"; then
        SKIP_REASONS="$SKIP_REASONS spam_sender "
    fi

    # Skip if spam
    if [ -n "$SKIP_REASONS" ]; then
        echo "   ⏭️  Skipping $ID ($SKIP_REASONS)"
        continue
    fi

    # Generate filename
    AUTHOR_NAME=$(echo "$email" | jq -r '.from[].name // "Neznámý"')
    OUTPUT_FILE=$(generate_filename "$SUBJECT" "$AUTHOR_NAME")

    echo "   🎙️  Creating podcast: $SUBJECT ($WORDS words, $FROM)"

    # Create podcast
    printf '%s' "$SUBJECT. Od: $AUTHOR_NAME ($FROM) $BODY" | say -v "$VOICE" -r "$RATE" -o "$OUTPUT_FILE"

    # Add metadata (if supported by macOS)
    if command -v sips &> /dev/null; then
        # Add basic metadata
        xattr -w "com.apple.metadata:kMDItemTitle" "$SUBJECT" "$OUTPUT_FILE" 2>/dev/null || true
    fi

    PROCESSED=$((PROCESSED + 1))
done

echo ""
echo "✅ Done! Created $PROCESSED podcasts."
echo "📁 Location: $OUTPUT_DIR"
