import json, requests, sys
sys.stdout.reconfigure(encoding='utf-8')

API_BASE = 'https://www.moltbook.com/api/v1'
api_key = 'moltbook_sk_xyNRkWz8Ctn-gqMeaKMO7W1SxEnsn2ps'
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

# Post ID with unread comments
post_id = '85b0910b-d945-4c50-969a-63efb4979a83'

# Try to get comments directly
print(f"=== Fetching Comments for Post: {post_id} ===")
resp = requests.get(f'{API_BASE}/posts/{post_id}/comments', headers=headers, timeout=30)
data = resp.json()

# Save response
with open('C:/Users/PC/.openclaw/workspace/memory/moltbook-comments-list.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(json.dumps(data, indent=2, ensure_ascii=False)[:5000])
