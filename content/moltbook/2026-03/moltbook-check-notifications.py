#!/usr/bin/env python3
"""Check Moltbook notifications"""
import json
import requests
import os
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Load API key
api_key = ''
cred_file = os.path.expanduser('~/.config/moltbook/credentials.json')
if os.path.exists(cred_file):
    with open(cred_file, 'r', encoding='utf-8') as f:
        creds = json.load(f)
        api_key = creds.get('api_key', '')

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

# Get notifications
resp = requests.get('https://www.moltbook.com/api/v1/notifications', headers=headers, timeout=30)
data = resp.json()

# Save to file for processing
output_file = os.path.expanduser('~/.openclaw/workspace/memory/moltbook-notifications.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

notifications = data.get('notifications', [])
print(f'Total notifications: {len(notifications)}')

# Count unread comments
unread_comments = [n for n in notifications if n.get('type') == 'comment' and not n.get('read', False)]
print(f'Unread comment notifications: {len(unread_comments)}')
print(f'Saved to {output_file}')
