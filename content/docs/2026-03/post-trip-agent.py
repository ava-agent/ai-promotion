import sys
sys.path.insert(0, 'C:/Users/PC/.openclaw/workspace/skills/moltbook-interact/scripts')
import moltbook

# Read post content (skip first 2 lines which are title)
with open('C:/Users/PC/.openclaw/workspace/memory/temp-trip-agent-post.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    title = lines[0].strip()
    body = ''.join(lines[2:]).strip()

# Create post
result = moltbook.create(title, body, 'general')
print(f"Result: {result}")
