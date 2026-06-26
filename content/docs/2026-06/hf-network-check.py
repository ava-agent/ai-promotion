#!/usr/bin/env python3
"""
检查HF Hub网络连接
"""

import requests
import sys

def check_network():
    print("[INFO] 检查HF Hub网络连接...")
    url = "https://huggingface.co/api/health"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"[SUCCESS] HF Hub可访问，状态码: {response.status_code}")
            print(f"[INFO] 响应内容: {response.text[:100]}")
            return True
        else:
            print(f"[WARNING] HF Hub返回异常状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] 无法访问HF Hub: {e}")
        return False

if __name__ == "__main__":
    success = check_network()
    sys.exit(0 if success else 1)
