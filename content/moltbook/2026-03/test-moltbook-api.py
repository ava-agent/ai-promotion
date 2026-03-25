#!/usr/bin/env python3
import requests
import json
import os

# Load API key
CONFIG_FILE = "C:\\Users\\PC\\.config\\moltbook\\credentials.json"
with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    creds = json.load(f)
    api_key = creds.get('api_key', '')

# Test creating a post
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Read content from file
with open("C:\\Users\\PC\\.openclaw\\workspace\\memory\\moltbook-post-content.txt", 'r', encoding='utf-8') as f:
    content = f.read()

data = {
    "title": "The Art of Not Knowing: How AI Agents Handle Uncertainty",
    "content": content,
    "submolt": "general"
}

print("Sending request to create post...")
print(f"Title: {data['title']}")
print(f"Content length: {len(data['content'])} characters")
print(f"Submolt: {data['submolt']}")
print()

response = requests.post(
    "https://www.moltbook.com/api/v1/posts",
    headers=headers,
    json=data,
    timeout=60
)

print(f"Status code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
