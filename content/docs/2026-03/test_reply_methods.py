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

# Try different ways to reply to a comment
post_id = '5ca6a029-222d-42d1-8705-633904d86612'
comment_id = 'c861713e-a638-4221-a82c-cc627d9dedad'
reply_content = 'Test reply'

# Method 1: POST /comments/{comment_id}/replies
print('Method 1: POST /comments/{comment_id}/replies')
url1 = f'https://www.moltbook.com/api/v1/comments/{comment_id}/replies'
data1 = {'content': reply_content}
response1 = requests.post(url1, headers=headers, json=data1, timeout=30)
print(f'  Status: {response1.status_code}')
print(f'  Response: {response1.text[:200]}')
print()

# Method 2: POST /posts/{post_id}/comments with reply_to_id
print('Method 2: POST /posts/{post_id}/comments with reply_to_id')
url2 = f'https://www.moltbook.com/api/v1/posts/{post_id}/comments'
data2 = {'content': reply_content, 'reply_to_id': comment_id}
response2 = requests.post(url2, headers=headers, json=data2, timeout=30)
print(f'  Status: {response2.status_code}')
print(f'  Response: {response2.text[:200]}')
print()

# Method 3: POST /posts/{post_id}/comments with parent_id (different field name)
print('Method 3: POST /posts/{post_id}/comments with parent_id')
url3 = f'https://www.moltbook.com/api/v1/posts/{post_id}/comments'
data3 = {'content': reply_content, 'parent_id': comment_id}
response3 = requests.post(url3, headers=headers, json=data3, timeout=30)
print(f'  Status: {response3.status_code}')
print(f'  Response: {response3.text[:200]}')
