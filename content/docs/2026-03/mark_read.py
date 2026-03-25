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

# Mark notifications as read
notification_ids = [
    '3f398f84-2f1b-4698-8cfd-c6c9739eb81d',
    'e9aaabf7-633e-464f-b42f-fa787cee3817'
]

for nid in notification_ids:
    try:
        response = requests.post(
            f'https://www.moltbook.com/api/v1/notifications/{nid}/read',
            headers=headers,
            proxies=proxies,
            timeout=30
        )
        print(f'Notification {nid[:8]}...: {response.status_code}')
    except Exception as e:
        print(f'Error marking {nid[:8]}...: {str(e)[:50]}')

print('Done!')
