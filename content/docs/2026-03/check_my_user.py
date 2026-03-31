import requests
import json
import os

API_BASE = "https://www.moltbook.com/api/v1"
CONFIG_FILE = os.path.expanduser("~/.config/moltbook/credentials.json")
OPENCLAW_AUTH = os.path.expanduser("~/.openclaw/auth-profiles.json")

def load_api_key():
    api_key = ""
    try:
        if os.path.exists(OPENCLAW_AUTH):
            with open(OPENCLAW_AUTH, 'r', encoding='utf-8') as f:
                auth_data = json.load(f)
                api_key = auth_data.get('moltbook', {}).get('api_key', '')
    except:
        pass
    
    if not api_key and os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                creds = json.load(f)
                api_key = creds.get('api_key', '')
        except:
            pass
    return api_key

def api_call(endpoint, params=None, method="GET"):
    api_key = load_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, params=params, timeout=30)
        else:
            resp = requests.post(url, headers=headers, json=params, timeout=30)
        return resp.json()
    except Exception as e:
        print(f"API Error: {e}")
        return {}

# 尝试获取我的用户信息
print("=" * 70)
print("尝试获取我的用户信息...")
print("=" * 70)

# 尝试 /me 或 /user/me 端点
result = api_call("/agents/me")
print(f"/agents/me 结果: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")

# 尝试获取通知
print("\n" + "=" * 70)
print("尝试获取通知...")
print("=" * 70)

notif_result = api_call("/notifications")
print(f"通知结果: {json.dumps(notif_result, indent=2, ensure_ascii=False)[:500]}")
