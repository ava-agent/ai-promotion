import requests
import json

# Read the article content
with open("article.md", "r", encoding="utf-8") as f:
    body_markdown = f.read()

# Dev.to API request
url = "https://dev.to/api/articles"
headers = {
    "Content-Type": "application/json",
    "api-key": "HThAUfdnNZPfreGabMMC9soa"
}
payload = {
    "article": {
        "title": "I Tried to Build a Decentralized AI Agent Marketplace. Here's What Broke (and What Worked)",
        "body_markdown": body_markdown,
        "published": True,
        "tags": ["ai", "agents", "blockchain", "typescript", "opensource"]
    }
}

response = requests.post(url, headers=headers, json=payload)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
