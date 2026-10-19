"""Publish an article using a privately supplied DEVTO_API_KEY."""

import os
from pathlib import Path
import sys


def publish_article(article_path="article.md"):
    api_key = os.environ.get("DEVTO_API_KEY", "").strip()
    if not api_key:
        print("Missing DEVTO_API_KEY; no request was sent.", file=sys.stderr)
        return 1

    try:
        body_markdown = Path(article_path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        print("Cannot read the article; no request was sent.", file=sys.stderr)
        return 1

    import requests

    payload = {
        "article": {
            "title": "I Tried to Build a Decentralized AI Agent Marketplace. Here's What Broke (and What Worked)",
            "body_markdown": body_markdown,
            "published": True,
            "tags": ["ai", "agents", "blockchain", "typescript", "opensource"],
        }
    }
    try:
        response = requests.post(
            "https://dev.to/api/articles",
            headers={"Content-Type": "application/json", "api-key": api_key},
            json=payload,
            timeout=30,
        )
    except requests.RequestException:
        # Exceptions and API bodies may echo credentials or private content.
        print("Dev.to request failed; response details withheld.", file=sys.stderr)
        return 1

    print(f"Status: {response.status_code}")
    return 0 if 200 <= response.status_code < 300 else 1


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python devto_publish.py [article.md]", file=sys.stderr)
        sys.exit(1)
    sys.exit(publish_article(sys.argv[1] if len(sys.argv) == 2 else "article.md"))
