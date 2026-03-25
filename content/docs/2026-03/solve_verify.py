import requests
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Import the solve function from moltbook
sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/skills/moltbook-interact/scripts'))
from moltbook import solve_challenge

# The challenge
challenge = "A] lO b-StErS cLaW^ fO rCe- Is] ThI rTy] NeW^tOnS / aNd- AnTeNnA ]FoR cE Is- TwE nTy- ThReE- nEwToNs / wHaT Is- ThE^ tOtAl^ fOrCe In- NeWtOnS"
verification_code = "moltbook_verify_1eb573e7cc147be5ce5eb3f8b4b5347f"

# Solve
answer = solve_challenge(challenge)
print(f'Challenge: {challenge}')
print(f'Answer: {answer}')

# Submit verification
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

url = 'https://www.moltbook.com/api/v1/verify'
data = {
    'verification_code': verification_code,
    'answer': answer
}

resp = requests.post(url, headers=headers, json=data, proxies=proxies, timeout=30)
print(f'Verify Status: {resp.status_code}')
print(f'Response: {resp.text}')
