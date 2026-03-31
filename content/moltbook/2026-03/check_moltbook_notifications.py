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

# Get full notifications
resp = requests.get('https://www.moltbook.com/api/v1/notifications', headers=headers, proxies=proxies, timeout=30)
data = resp.json()

# Write to file
with open('C:/Users/PC/.openclaw/workspace/memory/moltbook-notifications.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'Saved {len(data.get("notifications", []))} notifications to file')

# Print unread count
unread = [n for n in data.get('notifications', []) if not n.get('isRead', True)]
print(f'Unread: {len(unread)}')

# Show unread notifications summary
for n in unread:
    print(f"\n--- Unread Notification ---")
    print(f"Type: {n.get('type')}")
    print(f"Content: {n.get('content')}")
    post = n.get('post', {})
    if post:
        title = post.get('title', 'N/A')
        print(f"Post: {title[:80] if len(title) > 80 else title}")
    print(f"Post ID: {n.get('relatedPostId')}")
    print(f"Comment ID: {n.get('relatedCommentId')}")
    
    # Get comment details
    comment_id = n.get('relatedCommentId')
    post_id = n.get('relatedPostId')
    if comment_id and post_id:
        # Get post with comments
        post_resp = requests.get(f'https://www.moltbook.com/api/v1/posts/{post_id}', headers=headers, proxies=proxies, timeout=30)
        post_data = post_resp.json()
        comments = post_data.get('comments', [])
        for c in comments:
            if c.get('id') == comment_id:
                author = c.get('author', {}).get('name', 'Unknown')
                content = c.get('content', '')
                print(f"Comment Author: {author}")
                print(f"Comment Content: {content[:200]}...")
                break
