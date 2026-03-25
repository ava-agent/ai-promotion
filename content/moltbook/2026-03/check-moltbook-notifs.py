#!/usr/bin/env python3
import json
import requests
import os
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

API_BASE = 'https://www.moltbook.com/api/v1'
OPENCLAW_AUTH = os.path.expanduser('~/.openclaw/auth-profiles.json')

# Load API key
api_key = ''
with open(OPENCLAW_AUTH, 'r', encoding='utf-8') as f:
    auth_data = json.load(f)
    api_key = auth_data.get('moltbook', {}).get('api_key', '')

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

# Try to get notifications
response = requests.get(f'{API_BASE}/notifications', headers=headers, timeout=30)
data = response.json()

# Print summary
if 'notifications' in data:
    notifs = data['notifications']
    print(f'Total notifications: {len(notifs)}')
    
    unread = [n for n in notifs if not n.get('read', True)]
    print(f'Unread notifications: {len(unread)}')
    
    # Group by type
    type_counts = {}
    for n in notifs:
        t = n.get('type', 'unknown')
        type_counts[t] = type_counts.get(t, 0) + 1
    
    print(f'By type: {type_counts}')
    
    # Show unread comment replies
    comment_replies = [n for n in unread if n.get('type') == 'comment_reply']
    print(f'\n--- Unread Comment Replies ({len(comment_replies)}) ---')
    
    for i, n in enumerate(comment_replies[:10], 1):
        comment = n.get('comment', {})
        post = n.get('post', {})
        author = comment.get('author', {})
        
        print(f'{i}. Post: {post.get("title", "N/A")[:50]}')
        print(f'   Post ID: {post.get("id", "N/A")}')
        print(f'   From: {author.get("name", "unknown")}')
        content = comment.get('content', '')
        print(f'   Content: {content[:150]}...' if len(content) > 150 else f'   Content: {content}')
        print()
else:
    print('No notifications field found')
    print('Keys:', list(data.keys())[:10])
