import json, requests, sys
sys.stdout.reconfigure(encoding='utf-8')

API_BASE = 'https://www.moltbook.com/api/v1'
api_key = 'moltbook_sk_xyNRkWz8Ctn-gqMeaKMO7W1SxEnsn2ps'
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

# Get notifications
resp = requests.get(f'{API_BASE}/notifications', headers=headers, timeout=30)
data = resp.json()

# Save full data
with open('C:/Users/PC/.openclaw/workspace/memory/moltbook-notifications.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'Total notifications: {len(data.get("notifications", []))}')

# Print summary
for n in data.get('notifications', [])[:10]:
    ntype = n.get('type', 'N/A')
    content = n.get('content', 'N/A')
    is_read = n.get('isRead', False)
    post_id = n.get('relatedPostId', 'N/A')
    comment_id = n.get('relatedCommentId', 'N/A')
    print(f"Type: {ntype}")
    print(f"Content: {content}")
    print(f"Post ID: {post_id}")
    print(f"Comment ID: {comment_id}")
    print(f"Read: {is_read}")
    print("---")
