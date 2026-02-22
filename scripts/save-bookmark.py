#!/usr/bin/env python3
"""
Save bookmarks to Obsidian vault with auto-tagging and summary.
Usage: python3 save-bookmark.py <url> [tags...]
Example: python3 save-bookmark.py https://example.com/ai-agents #ai #agents
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path

# Obsidian vault path (přizpůsob podle svého setupu)
OBSIDIAN_VAULT = Path("~/Documents/ObsidianVault").expanduser()
BOOKMARKS_DIR = OBSIDIAN_VAULT / "Bookmarks"

# Default tags pro různé témata
DEFAULT_TAGS = {
    "ai": ["#ai", "#agents"],
    "dev": ["#dev", "#tools"],
    "design": ["#design", "#ux"],
    "productivity": ["#productivity", "#workflow"],
    "business": ["#business", "#entrepreneur"],
    "video": ["#youtube", "#content"],
}

def extract_tags(text):
    """Extract tags from text like #ai, #dev, etc."""
    return re.findall(r'#(\w+)', text.lower())

def guess_tags_from_url(url):
    """Guess tags based on URL content."""
    url_lower = url.lower()
    tags = []
    if any(x in url_lower for x in ["youtube", "video"]):
        tags.append("#video")
    if any(x in url_lower for x in ["github", "gitlab", "bitbucket"]):
        tags.append("#dev")
    if any(x in url_lower for x in ["medium", "substack", "blog"]):
        tags.append("#writing")
    return tags

def create_bookmark_file(url, title=None, summary=None, tags=None):
    """Create an Obsidian bookmark note."""
    today = datetime.now().strftime("%Y-%m-%d")
    slug = re.sub(r'[^a-z0-9]+', '-', url.lower().strip('/'))[:50]
    filename = f"{today}-{slug}.md"
    filepath = BOOKMARKS_DIR / filename

    # Build content
    content = f"""---
url: {url}
date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
tags: {', '.join(tags or [])}
---

# {title or url}

> {summary or 'No summary available.'}

---

Original: [{url}]({url})
"""
    # Ensure directory exists
    BOOKMARKS_DIR.mkdir(parents=True, exist_ok=True)

    # Write file
    filepath.write_text(content)
    return filepath

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 save-bookmark.py <url> [tags...]")
        sys.exit(1)

    url = sys.argv[1]
    provided_tags = sys.argv[2:] if len(sys.argv) > 2 else []

    # Combine tags
    all_tags = provided_tags or guess_tags_from_url(url)
    if not all_tags:
        all_tags = ["#bookmark"]

    # TODO: Fetch title and summary from URL
    # For now, use a placeholder
    filepath = create_bookmark_file(
        url=url,
        title=None,
        summary="TODO: Fetch summary from URL",
        tags=all_tags
    )
    print(f"✅ Bookmark saved: {filepath}")

if __name__ == "__main__":
    main()
