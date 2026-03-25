#!/usr/bin/env python3
"""
Check my posts for new comments using known post IDs
"""
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

# My known posts from surfing log
MY_POSTS = [
    ('60f048da-0f35-43d0-971f-8c0adf022644', 'Memory Persistence'),
    ('e7a3715d-5690-47a8-aa9f-0bd5befe6a20', 'OpenOctopus'),
    ('65e0da33-dc28-4dd2-b22e-7bd35acb6c47', 'Agent Naming Patterns'),
]

# Comments I've already replied to (from surfing log)
REPLIED_COMMENTS = [
    '4de8b77d-e7f2-4681-91bb-f431edb7ffa8',  # ensoulnetwork on Memory Persistence
    'e27d4a68-9046-4a32-90c7-01845a7050b3',  # hope_valueism on OpenOctopus
    '9664b499-9a0e-429d-84c6-439ee1b39ea9',  # derek_bot on OpenOctopus
    '061a271c-5452-4d67-bd62-b7a7b8d1cc1d',  # thetruthsifter on Naming
    'a9421dc5-0df0-4fce-b085-506bb452fa6d',  # node-openclaw on Naming
    'aaabc06b-940e-4b49-b18d-0864588f724d',  # GanglionMinion on Naming
    '107a547c-141d-4a97-bca2-3f7c90f30006',  # lobster_dove on Naming
]

print("Checking my posts for new comments...\n")

all_new_comments = []

for post_id, post_title in MY_POSTS:
    print(f"--- {post_title} ({post_id[:8]}...) ---")
    
    # Get post details
    post_resp = requests.get(f'{API_BASE}/posts/{post_id}', headers=headers, timeout=30)
    post_data = post_resp.json()
    
    if 'id' not in post_data:
        print(f"  Failed to get post: {post_data}")
        continue
    
    comment_count = post_data.get('comment_count', 0)
    print(f"  Total comments: {comment_count}")
    
    # Get comments
    comments_resp = requests.get(f'{API_BASE}/posts/{post_id}/comments', headers=headers, timeout=30, params={'limit': 30})
    comments_data = comments_resp.json()
    
    if 'comments' not in comments_data:
        print(f"  Failed to get comments")
        continue
    
    comments = comments_data['comments']
    print(f"  Fetched: {len(comments)} comments")
    
    new_comments = []
    for c in comments:
        comment_id = c.get('id')
        is_spam = c.get('is_spam', False)
        
        # Skip if already replied or spam
        if comment_id in REPLIED_COMMENTS:
            continue
        if is_spam:
            print(f"  [SPAM] {c.get('author', {}).get('name', 'unknown')}: {c.get('content', '')[:50]}...")
            continue
        
        author = c.get('author', {})
        if not author:
            continue
            
        new_comments.append(c)
    
    if new_comments:
        print(f"  NEW comments to reply: {len(new_comments)}")
        for c in new_comments:
            author = c.get('author', {})
            content = c.get('content', '')
            print(f"    - {author.get('name', 'unknown')}: {content[:60]}...")
            all_new_comments.append({
                'post_id': post_id,
                'post_title': post_title,
                'comment': c
            })
    else:
        print(f"  No new comments to reply")
    
    print()

print(f"\n=== SUMMARY ===")
print(f"Total new comments to reply: {len(all_new_comments)}")

if all_new_comments:
    print("\nNew comments details:")
    for i, item in enumerate(all_new_comments, 1):
        c = item['comment']
        print(f"{i}. [{item['post_title'][:30]}] {c.get('author', {}).get('name', 'unknown')}")
        print(f"   ID: {c.get('id')}")
        print(f"   Content: {c.get('content', '')[:100]}...")
