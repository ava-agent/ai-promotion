import requests
import json
import os

print('HF Token Verification Started...')
print()

# Try to get token from file or environment
token_file = 'memory/hf-token.txt'
api_token = None

# Try to read token from file
try:
    with open(token_file, 'r') as f:
        api_token = f.read().strip()
        print(f'Token found in file: {api_token[:20]}...' if api_token else 'No token found in file')
except:
    print('Token file not found')

# If not from file, try environment variable
if not api_token:
    print('Trying to get token from environment variable...')
    api_token = os.environ.get('HF_TOKEN')
    if api_token:
        print(f'Token from environment: {api_token[:20]}...')
    else:
        print('No token found in environment variable')

# If still no token, check if we can proceed without it
if not api_token:
    print('Warning: No HF Token found')
    print('Will proceed with public API access only')
    api_token = None

print()
print('Starting token verification...')
print()

if api_token:
    try:
        headers = {
            'Authorization': f'Bearer {api_token}',
            'User-Agent': 'OpenClaw-HF-Monitor'
        }
        
        # Get user info
        response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_info = response.json()
            print('Token is valid')
            print(f'Username: {user_info.get("name", "Unknown")}')
            print(f'Organization: {user_info.get("organization", "None")}')
            print(f'Type: {user_info.get("type", "Unknown")}')
            
            # Check organization access
            orgs = user_info.get('organizations', [])
            if 'IKUN-LLM' in orgs:
                print('IKUN-LLM organization access: OK')
            else:
                print('IKUN-LLM organization access: Not available')
                
            success = True
        else:
            print(f'Token invalid, status code: {response.status_code}')
            print(f'Error: {response.text}')
            success = False
            
    except Exception as e:
        print(f'Token verification failed: {str(e)}')
        success = False
else:
    print('Proceeding without token - using public API access')
    success = True