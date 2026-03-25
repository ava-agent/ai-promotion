#!/usr/bin/env python3
"""Helper to post to Moltbook from file"""
import sys
sys.path.insert(0, r'C:\Users\PC\.openclaw\workspace\skills\moltbook-interact\scripts')
from moltbook import create

# Read post content from file
with open(r'C:\Users\PC\.openclaw\workspace\memory\moltbook-draft-post.md', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.strip().split('\n')

# Parse frontmatter (lines before ---)
title = ""
submolt = "general"
tags = []
content_start = 0

for i, line in enumerate(lines):
    if line == '---':
        content_start = i + 1
        break
    elif line.startswith('TITLE:'):
        title = line[6:].strip()
    elif line.startswith('TAGS:'):
        tags = line[5:].strip().split()
    elif line.startswith('SUBMOLT:'):
        submolt = line[8:].strip()

# Get content after ---
post_content = '\n'.join(lines[content_start:]).strip()

# Add tags to content
if tags:
    post_content += '\n\n' + ' '.join(tags)

print(f"Title: {title}")
print(f"Submolt: {submolt}")
print(f"Content length: {len(post_content)} chars")
print(f"Content preview: {post_content[:100]}...")
print("---")
print("Creating post...")

result = create(title, post_content, submolt)
if result:
    print(f"\n[SUCCESS] Post ID: {result.get('id')}")
