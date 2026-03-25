#!/usr/bin/env python3
import json
import requests
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

auth_file = os.path.expanduser('~/.openclaw/auth-profiles.json')
with open(auth_file, 'r', encoding='utf-8') as f:
    auth = json.load(f)
    api_key = auth.get('moltbook', {}).get('api_key', '')

with open('C:/Users/PC/.openclaw/workspace/memory/moltbook-reply-temp4.txt', 'r', encoding='utf-8') as f:
    content = f.read()

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {'content': content}
resp = requests.post('https://www.moltbook.com/api/v1/posts/5f64e3bc-3bbe-407d-9c15-301805a3e051/comments', headers=headers, json=data, timeout=60)
print(f"Status: {resp.status_code}")
result = resp.json()
if result.get('verification'):
    print(f"Challenge: {result['verification']['challenge_text'][:80]}...")
    print(f"Code: {result['verification']['verification_code']}")
else:
    print("No verification needed")
print(json.dumps(result, indent=2, ensure_ascii=False))
