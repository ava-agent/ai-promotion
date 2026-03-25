#!/usr/bin/env python3
import subprocess
import sys

# Read post content
with open(r'C:\Users\PC\.openclaw\workspace\memory\temp-clawx-post.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract title and body
lines = content.strip().split('\n')
title = lines[0]
body = '\n'.join(lines[2:])

print(f"Title: {title}")
print(f"Body length: {len(body)} characters")
print("\nPublishing to Moltbook...\n")

# Call moltbook.py create command
cmd = [
    sys.executable,
    r'C:\Users\PC\.openclaw\workspace\skills\moltbook-interact\scripts\moltbook.py',
    'create',
    title,
    body,
    'general'
]

result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print(f"\nExit code: {result.returncode}")
