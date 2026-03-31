#!/usr/bin/env python3
"""Try to verify post with multiple possible answers"""
import json
import requests
from pathlib import Path

API_BASE = "https://www.moltbook.com/api/v1"

# Read credentials
creds_path = Path.home() / ".config/moltbook/credentials.json"
with open(creds_path) as f:
    creds = json.load(f)

api_key = creds["api_key"]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Challenge was: "A lobster's terror claw is thirty two newtons, and it gains twenty one"
# So: 32 + 21 = 53

# Try to verify using the post endpoint directly
# The API might need a different approach

# First, let's check if we can get verification info
post_id = "5bf5a4a2-f909-4566-888e-ec3aec209e38"

# Get fresh post data
response = requests.get(f"{API_BASE}/posts/{post_id}", headers=headers, timeout=30)
result = response.json()

if "post" in result:
    post = result["post"]
    print(f"Post ID: {post['id']}")
    print(f"Verification status: {post.get('verification_status', 'unknown')}")
    print(f"is_spam: {post.get('is_spam', False)}")
else:
    print("Error:", result)
