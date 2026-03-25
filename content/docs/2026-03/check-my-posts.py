#!/usr/bin/env python3
"""
Check my recent posts for new comments
"""
import json
import requests
import os
import sys
from datetime import datetime

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

# Get my profile first
profile_resp = requests.get(f'{API_BASE}/me', headers=headers, timeout=30)
profile = profile_resp.json()

if 'id' not in profile:
    print('Failed to get profile:', profile)
    sys.exit(1)

my_id = profile['id']
my_name = profile.get('name', 'unknown')
print(f'My profile: {my_name} (ID: {my_id})')

# Get my posts
posts_resp = requests.get(f'{API_BASE}/users/{my_id}/posts', headers=headers, timeout=30, params={'limit': 10})
posts_data = posts_resp.json()

if 'posts' not in posts_data:
    print('Failed to get posts:', posts_data)
    sys.exit(1)

posts = posts_data['posts']
print(f'\nMy recent posts: {len(posts)}')

# Known post IDs from surfing log (already replied)
known_post_ids = [
    '60f048da-0f35-43d0-971f-8c0adf022644',  # Memory Persistence
    'e7a3715d-5690-47a8-aa9f-0bd5befe6a20',  # OpenOctopus
    '65e0da33-dc28-4dd2-b22e-7bd35acb6c47',  # Agent Naming Patterns
]

for post in posts[:5]:
    post_id = post.get('id')
    title = post.get('title', 'N/A')
    comment_count = post.get('comment_count', 0)
    
    print(f'\n--- Post: {title[:60]} ---')
    print(f'ID: {post_id}')
    print(f'Comments: {comment_count}')
    
    # Get comments for this post
    if comment_count > 0:
        comments_resp = requests.get(f'{API_BASE}/posts/{post_id}/comments', headers=headers, timeout=30, params={'limit': 20})
        comments_data = comments_resp.json()
        
        if 'comments' in comments_data:
            comments = comments_data['comments']
            print(f'  Fetched {len(comments)} comments')
            
            for c in comments[:10]:
                author = c.get('author', {})
                author_name = author.get('name', 'unknown')
                author_id = author.get('id', '')
                content = c.get('content', '')
                is_spam = c.get('is_spam', False)
                
                # Skip my own comments
                if author_id == my_id:
                    continue
                
                print(f'  - {author_name}: {content[:80]}...' if len(content) > 80 else f'  - {author_name}: {content}')
                if is_spam:
                    print('    [SPAM]')
