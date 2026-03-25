import requests
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

api_key = 'moltbook_sk_xyNRkWz8Ctn-gqMeaKMO7W1SxEnsn2ps'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Delete test comment
comment_id = '14ed214a-cdcb-4373-b753-8ecda939640f'
url = f'https://www.moltbook.com/api/v1/comments/{comment_id}'

response = requests.delete(url, headers=headers, timeout=30)
print(f'Status: {response.status_code}')
print(f'Response: {response.text[:200]}')
