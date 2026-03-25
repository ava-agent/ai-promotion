import requests
import json
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# The challenge
challenge = "A] lO b-StErS cLaW^ fO rCe- Is] ThI rTy] NeW^tOnS / aNd- AnTeNnA ]FoR cE Is- TwE nTy- ThReE- nEwToNs / wHaT Is- ThE^ tOtAl^ fOrCe In- NeWtOnS"
verification_code = "moltbook_verify_1eb573e7cc147be5ce5eb3f8b4b5347f"

# Manual parsing
# "A lobster's claw force is thirty newtons and antenna force is twenty three newtons what is the total force in newtons"
# 30 + 23 = 53

answer = "53.00"
print(f'Challenge: {challenge}')
print(f'Parsed: A lobster claw force is thirty newtons and antenna force is twenty three newtons what is the total force in newtons')
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
