import requests
import sys

try:
    response = requests.get("https://huggingface.co/api/health", timeout=10)
    if response.status_code == 200:
        print("[OK] HF Hub is accessible")
        print(f"[INFO] Status code: {response.status_code}")
        print(f"[INFO] Response: {response.text[:100]}")
    else:
        print(f"[WARN] HF Hub returned status code: {response.status_code}")
except Exception as e:
    print(f"[ERROR] Cannot access HF Hub: {e}")
    sys.exit(1)
