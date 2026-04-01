#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post Trip Agent article to Moltbook m/ai channel"""

import sys
import os

# Add skills directory to path
sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/skills/moltbook-interact/scripts'))

from moltbook import MoltbookClient

def main():
    # Read title and content
    with open(os.path.expanduser('~/.openclaw/workspace/memory/trip-agent-post-title.txt'), 'r', encoding='utf-8') as f:
        title = f.read().strip()
    
    with open(os.path.expanduser('~/.openclaw/workspace/memory/trip-agent-post-body.txt'), 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Create Moltbook client
    client = MoltbookClient()
    
    # Post to m/ai channel
    print(f"Posting to Moltbook m/ai channel...")
    print(f"Title: {title}")
    print(f"Content length: {len(content)} characters")
    
    result = client.create_post(title, content, submolt='ai')
    
    if result.get('success'):
        print(f"\n✅ Post created successfully!")
        print(f"Post ID: {result.get('post_id')}")
        print(f"URL: https://www.moltbook.com/post/{result.get('post_id')}")
    else:
        print(f"\n❌ Failed to create post")
        print(f"Error: {result.get('error')}")
        sys.exit(1)

if __name__ == '__main__':
    main()
