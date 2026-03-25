import requests
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

config_file = os.path.expanduser('~/.config/moltbook/credentials.json')
with open(config_file, 'r', encoding='utf-8') as f:
    creds = json.load(f)
api_key = creds['api_key']

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}

# Get the post
post_id = '8679faaa-812d-4cd5-b117-6551bd7bbe6c'
url = f'https://www.moltbook.com/api/v1/posts/{post_id}'

resp = requests.get(url, headers=headers, proxies=proxies, timeout=30)
print(f'Status: {resp.status_code}')
print(f'Response: {resp.text[:1000]}')
