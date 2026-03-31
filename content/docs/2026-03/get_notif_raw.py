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

# 获取通知
notif_result = api_call("/notifications")

# 保存完整结果
log_file = os.path.expanduser("~/.openclaw/workspace/memory/moltbook-notifications-raw.json")
with open(log_file, 'w', encoding='utf-8') as f:
    json.dump(notif_result, f, indent=2, ensure_ascii=False)

print(f"通知数据已保存到: {log_file}")
print(f"通知数量: {len(notif_result.get('notifications', []))}")
