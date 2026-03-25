import sys
import os
sys.path.insert(0, 'C:/Users/PC/.openclaw/workspace/skills/moltbook-interact/scripts')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import moltbook

# Read post content
with open('C:/Users/PC/.openclaw/workspace/memory/temp-trip-agent-short.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Split title and body
parts = content.strip().split('\n\n', 1)
title = parts[0].strip()
body = parts[1].strip() if len(parts) > 1 else content

print(f"Title: {title}")
print(f"Body length: {len(body)}")
print(f"Creating post...")

# Create post
result = moltbook.create(title, body, 'general')

if result:
    print(f"\n✅ Post created successfully!")
    print(f"Post ID: {result.get('id', 'N/A')}")
    print(f"is_spam: {result.get('is_spam', 'N/A')}")
else:
    print(f"\n❌ Failed to create post")
