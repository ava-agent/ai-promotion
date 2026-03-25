#!/usr/bin/env python3
"""Reply to valid Moltbook comments"""
import json
import requests
import os
import sys
import time

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

# Load notifications
notif_file = os.path.expanduser('~/.openclaw/workspace/memory/moltbook-notifications.json')
with open(notif_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

notifications = data.get('notifications', [])

# Filter valid comments
valid_comments = []
for n in notifications:
    if n.get('type') != 'post_comment':
        continue
    
    comment = n.get('comment', {})
    post = n.get('post', {})
    
    # Skip spam/crypto
    if comment.get('isSpam', False) or comment.get('isCrypto', False):
        continue
    
    content = comment.get('content', '')
    
    # Skip short/generic comments
    if len(content) < 30:
        continue
    
    # Skip very generic phrases
    generic_phrases = ['Great post!', 'Keep it up!', 'Quality post', 'Strong community', 
                       'This is the way!', 'Underrated take', 'Interesting take']
    if any(phrase in content for phrase in generic_phrases):
        continue
    
    valid_comments.append({
        'comment_id': comment.get('id'),
        'post_id': n.get('relatedPostId'),
        'content': content[:200],
        'post_title': post.get('title', 'Unknown')[:50],
        'author_id': comment.get('authorId')
    })

print(f'Total notifications: {len(notifications)}')
print(f'Valid comments to reply: {len(valid_comments)}')
print()

for i, c in enumerate(valid_comments, 1):
    print(f'{i}. Post: {c["post_title"]}')
    print(f'   Comment: {c["content"][:100]}...')
    print()

# Save valid comments for manual review
output_file = os.path.expanduser('~/.openclaw/workspace/memory/moltbook-valid-comments.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(valid_comments, f, indent=2, ensure_ascii=False)
print(f'Saved to {output_file}')
