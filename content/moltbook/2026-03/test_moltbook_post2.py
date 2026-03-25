import requests
import json
import os
import sys

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Load credentials
config_file = os.path.expanduser('~/.config/moltbook/credentials.json')
with open(config_file, 'r', encoding='utf-8') as f:
    creds = json.load(f)
api_key = creds['api_key']

# API settings - NO PROXY
url = 'https://www.moltbook.com/api/v1/posts'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Read the actual post content
content_file = os.path.expanduser('~/.openclaw/workspace/memory/temp-openoctopus-post.md')
with open(content_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the first line (title) since we pass it separately
lines = content.strip().split('\n')
title = lines[0].replace('# ', '')
body = '\n'.join(lines[1:]).strip()

print(f'Title: {title}')
print(f'Content length: {len(body)} chars')

# Create post - NO PROXY
data = {
    'title': title,
    'content': body,
    'submolt': 'general'
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=60)
    print(f'Status: {response.status_code}')
    
    # Try to get response text
    try:
        result = response.json()
        print(f'Success: {result.get("success")}')
        
        if 'post' in result:
            post = result['post']
            print(f'Post ID: {post.get("id")}')
            
            # Check for verification
            verification = result.get('verification') or post.get('verification')
            if verification:
                print('Verification required!')
                challenge_text = verification.get('challenge_text', '')
                verification_code = verification.get('verification_code', '')
                print(f'Challenge: {challenge_text[:80]}...')
                print(f'Code: {verification_code}')
        else:
            print(f'Error: {result}')
    except:
        print(f'Response text: {response.text[:200]}')
        
except Exception as e:
    print(f'Error: {e}')
