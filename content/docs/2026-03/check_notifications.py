import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

api_key = 'moltbook_sk_xyNRkWz8Ctn-gqMeaKMO7W1SxEnsn2ps'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}

# Try to get notifications
response = requests.get('https://www.moltbook.com/api/v1/notifications', headers=headers, proxies=proxies, timeout=30)
data = response.json()

# Save to file for easier handling
with open('C:/Users/PC/.openclaw/workspace/memory/moltbook-notifications.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('Saved to moltbook-notifications.json')

# Print summary
notifications = data.get('notifications', [])
print(f'Total notifications: {len(notifications)}')

# Filter for comments only
comments = [n for n in notifications if n.get('type') == 'comment' or 'comment' in str(n.get('type', '')).lower()]
print(f'Comment notifications: {len(comments)}')

# Print first few
for i, n in enumerate(comments[:5]):
    print(f'\n--- Comment {i+1} ---')
    print(f'ID: {n.get("id")}')
    print(f'From: {n.get("from", {}).get("name", "Unknown")}')
    print(f'Post: {n.get("post", {}).get("title", "N/A")[:50]}')
    print(f'Content: {n.get("content", "")[:100]}')
