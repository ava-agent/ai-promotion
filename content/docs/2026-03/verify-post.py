import requests
import json
import os

# Load API key
OPENCLAW_AUTH = os.path.expanduser("~/.openclaw/auth-profiles.json")
with open(OPENCLAW_AUTH, 'r', encoding='utf-8') as f:
    auth_data = json.load(f)
    api_key = auth_data.get('moltbook', {}).get('api_key', '')

# Post ID and verification code
post_id = 'b15db331-c059-4933-a6fc-321520b869d0'
answer = '25.00'

# First, get the post to retrieve the verification code
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Get post details
response = requests.get(f"https://www.moltbook.com/api/v1/posts/{post_id}", headers=headers)
post_data = response.json()

if 'post' in post_data:
    print(f"Post found: {post_data['post']['title']}")
    print(f"Verification status: {post_data['post'].get('verification_status', 'N/A')}")
    
    # Try to verify with the correct answer
    verify_data = {
        "post_id": post_id,
        "answer": answer
    }
    
    verify_response = requests.post(
        "https://www.moltbook.com/api/v1/verify",
        headers=headers,
        json=verify_data
    )
    
    print(f"\nVerification response: {verify_response.json()}")
else:
    print(f"Error: {post_data}")
