#!/usr/bin/env python3
import requests
import json
import os
import sys

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Load API key
auth_file = os.path.expanduser('~/.openclaw/auth-profiles.json')
with open(auth_file, 'r', encoding='utf-8') as f:
    auth_data = json.load(f)
    api_key = auth_data.get('moltbook', {}).get('api_key', '')

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}

# Mark all unread notifications as read
notification_ids = [
    "5e4f7b6f-01ed-42b4-9900-1f7acb318ad1",  # post_comment
    "718896fb-161c-48c6-9942-bab365b91c36",  # comment_reply
    "91e787cf-f87b-4dab-b2f4-e86a8b5c4b8e",  # comment_reply
    "361e03f3-d92b-48a8-b137-64bdb306c807",  # comment_reply
    "60fcc06e-d052-4264-82b1-054160e04004",  # comment_reply
    "9602fe13-d130-45a7-ac60-7894c8269843",  # comment_reply
    "3e9979af-015a-49f1-92b2-7ccc0c400775",  # comment_reply
    "35a9e5ef-8600-4eb3-9a3b-a1a992f10603",  # comment_reply
    "74262959-ece2-4674-9cf9-548eae7d640c",  # comment_reply
    "baaccd61-35b5-4fb4-a11f-900989d7a3ed",  # comment_reply
    "ca239d5b-39e4-42b3-b375-230a8f94ec12",  # comment_reply
    "ae31853e-f197-4018-954d-6b29288b3363",  # comment_reply
]

for nid in notification_ids:
    try:
        resp = requests.post(
            f'https://www.moltbook.com/api/v1/notifications/{nid}/read',
            headers=headers,
            proxies=proxies,
            timeout=30
        )
        if resp.status_code == 200:
            print(f"[OK] Marked {nid[:8]}... as read")
        else:
            print(f"[WARN] Failed to mark {nid[:8]}...: {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] {nid[:8]}...: {str(e)[:50]}")

print("\nDone!")
