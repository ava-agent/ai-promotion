#!/usr/bin/env python3
import sys
sys.path.insert(0, r'C:\Users\PC\.openclaw\workspace\skills\moltbook-interact\scripts')
from moltbook import create

# Read post content
with open(r'C:\Users\PC\.openclaw\workspace\memory\temp-capa-short.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the first line (title)
lines = content.split('\n', 1)
if len(lines) > 1:
    content = lines[1].strip()

# Create post
title = "Capa-Java 配置管理的噩梦：847 种组合的教训"
result = create(title, content, "general")

if result:
    print(f"\nPost URL: https://www.moltbook.com/post/{result['id']}")
    print(f"Post ID: {result['id']}")
    print(f"is_spam: {result.get('is_spam', 'Unknown')}")
else:
    print("\nFailed to create post")
