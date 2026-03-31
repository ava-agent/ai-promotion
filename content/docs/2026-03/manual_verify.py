#!/usr/bin/env python3
"""Manual verification for a post"""
import sys
import json
import requests
from pathlib import Path

API_BASE = "https://www.moltbook.com/api/v1"

# Read credentials
creds_path = Path.home() / ".config/moltbook/credentials.json"
with open(creds_path) as f:
    creds = json.load(f)

api_key = creds["api_key"]

# First, get the post to find verification_code
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Get post details
post_url = f"{API_BASE}/posts/5bf5a4a2-f909-4566-888e-ec3aec209e38"
response = requests.get(post_url, headers=headers, timeout=30)
post_data = response.json()

print("Post status:", post_data.get("verification_status"))
print("Full post:", json.dumps(post_data, indent=2)[:500])
