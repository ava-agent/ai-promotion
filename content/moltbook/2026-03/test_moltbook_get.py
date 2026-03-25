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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}

# Test GET
print('Testing GET /posts...')
url = 'https://www.moltbook.com/api/v1/posts'
resp = requests.get(url, headers=headers, params={'sort': 'hot', 'limit': 1}, proxies=proxies, timeout=30)
print(f'GET Status: {resp.status_code}')
if resp.status_code == 200:
    print('GET works!')

# Test minimal POST with proxy
print('\nTesting POST /posts with minimal content...')
url = 'https://www.moltbook.com/api/v1/posts'
data = {'title': 'Test', 'content': 'Test content', 'submolt': 'general'}
resp = requests.post(url, headers=headers, json=data, proxies=proxies, timeout=30)
print(f'POST Status: {resp.status_code}')
print(f'Response: {resp.text[:200]}')
