#!/usr/bin/env python3
"""
Filter high-quality comments and prepare replies
"""
import json
import sys
import os

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Load comments
with open('C:/Users/PC/.openclaw/workspace/memory/new-comments-to-reply.json', 'r', encoding='utf-8') as f:
    all_comments = json.load(f)

print(f"Total comments: {len(all_comments)}\n")

# Filter criteria
SPAM_AUTHORS = ['coinflipcasino', 'doriangrey']  # Known spam authors
MIN_CONTENT_LENGTH = 100  # Minimum characters for quality comment

high_quality = []

for item in all_comments:
    comment = item['comment']
    author_name = comment.get('author', {}).get('name', '')
    content = comment.get('content', '')
    is_deleted = comment.get('is_deleted', False)
    is_spam = comment.get('is_spam', False)
    
    # Skip deleted
    if is_deleted:
        continue
    
    # Skip spam authors
    if author_name in SPAM_AUTHORS:
        continue
    
    # Skip spam flagged
    if is_spam:
        continue
    
    # Skip short comments
    if len(content) < MIN_CONTENT_LENGTH:
        continue
    
    # Skip "Deleted comment" content
    if 'Deleted comment' in content:
        continue
    
    high_quality.append(item)

print(f"High-quality comments to reply: {len(high_quality)}\n")

# Group by post
by_post = {}
for item in high_quality:
    post_title = item['post_title']
    if post_title not in by_post:
        by_post[post_title] = []
    by_post[post_title].append(item)

for post_title, comments in by_post.items():
    print(f"=== {post_title} ({len(comments)} comments) ===")
    for item in comments[:5]:  # Show first 5 per post
        c = item['comment']
        author = c.get('author', {}).get('name', 'unknown')
        content = c.get('content', '')
        print(f"  [{author}] {content[:100]}...")
        print(f"  ID: {c.get('id')}")
        print()
