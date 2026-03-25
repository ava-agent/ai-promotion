import requests
import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

api_key = 'moltbook_sk_xyNRkWz8Ctn-gqMeaKMO7W1SxEnsn2ps'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Get comments for the post
post_id = '5ca6a029-222d-42d1-8705-633904d86612'
url = f'https://www.moltbook.com/api/v1/posts/{post_id}/comments'

response = requests.get(url, headers=headers, timeout=30)
data = response.json()

# Save to file
with open('post-comments.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

comment_count = len(data.get('comments', []))
print(f'Saved {comment_count} comments')
