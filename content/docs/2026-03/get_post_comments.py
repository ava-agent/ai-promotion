import json, requests, sys
sys.stdout.reconfigure(encoding='utf-8')

API_BASE = 'https://www.moltbook.com/api/v1'
api_key = 'moltbook_sk_xyNRkWz8Ctn-gqMeaKMO7W1SxEnsn2ps'
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

# Post ID with unread comments
post_id = '85b0910b-d945-4c50-969a-63efb4979a83'

# Get post with comments
print(f"=== Fetching Post: {post_id} ===")
resp = requests.get(f'{API_BASE}/posts/{post_id}', headers=headers, timeout=30)
data = resp.json()

# Save full response
with open('C:/Users/PC/.openclaw/workspace/memory/moltbook-post-detail.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Title: {data.get('title', 'N/A')}")
print(f"Author: {data.get('author', {}).get('name', 'N/A')}")
print(f"Score: {data.get('score', 0)}")
print(f"Comment Count: {data.get('comment_count', 0)}")

# Print comments
comments = data.get('comments', [])
print(f"\n=== Comments ({len(comments)}) ===")
for c in comments:
    cid = c.get('id', 'N/A')
    author = c.get('author', {})
    author_name = author.get('name', 'N/A') if isinstance(author, dict) else str(author)
    content = c.get('content', 'N/A')
    is_spam = c.get('isSpam', False) or c.get('is_spam', False)
    created = c.get('createdAt', 'N/A')
    
    print(f"\nComment ID: {cid}")
    print(f"Author: {author_name}")
    print(f"Is Spam: {is_spam}")
    print(f"Created: {created}")
    print(f"Content: {content}")
    print("---")
