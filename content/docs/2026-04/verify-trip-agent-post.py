#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Moltbook post manually"""

import sys
import os
import json
import requests

# Configuration
API_BASE = "https://www.moltbook.com/api/v1"
PROXY_HOST = "127.0.0.1"
PROXY_PORT = "7897"
PROXY_ENABLED = True

def load_api_key():
    """Load API key from OpenClaw auth or credentials file"""
    api_key = ""
    
    # Try OpenClaw auth first
    openclaw_auth = os.path.expanduser("~/.openclaw/auth.json")
    if os.path.exists(openclaw_auth):
        try:
            with open(openclaw_auth, 'r', encoding='utf-8') as f:
                auth_data = json.load(f)
                api_key = auth_data.get('moltbook', {}).get('api_key', '')
        except:
            pass
    
    if not api_key:
        config_file = os.path.expanduser("~/.config/moltbook/credentials.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    creds = json.load(f)
                    api_key = creds.get('api_key', '')
            except:
                pass
    
    return api_key

def verify_post(verification_code, answer):
    """Submit verification answer"""
    api_key = load_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "verification_code": verification_code,
        "answer": answer
    }
    
    proxies = None
    if PROXY_ENABLED:
        proxies = {
            "http": f"http://{PROXY_HOST}:{PROXY_PORT}",
            "https": f"http://{PROXY_HOST}:{PROXY_PORT}"
        }
    
    url = f"{API_BASE}/verify"
    response = requests.post(url, headers=headers, json=data, proxies=proxies, timeout=60)
    return response.json()

# Post ID and verification code from the failed attempt
post_id = "3d607825-390b-401d-94eb-cafce9404262"
# We need to get the verification code from the post creation response
# Since we don't have it, let's try to get the post details

api_key = load_api_key()
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

proxies = {
    "http": f"http://{PROXY_HOST}:{PROXY_PORT}",
    "https": f"http://{PROXY_HOST}:{PROXY_PORT}"
}

# Get post details
url = f"{API_BASE}/posts/{post_id}"
response = requests.get(url, headers=headers, proxies=proxies, timeout=60)
post_data = response.json()

print(json.dumps(post_data, indent=2))
