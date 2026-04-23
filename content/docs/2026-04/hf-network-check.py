#!/usr/bin/env python3
"""
Hugging Face 网络连接检查脚本
用于验证HF Hub的网络连接状态
"""

import requests
import time
import sys

def check_hf_connection():
    """检查HF连接状态"""
    print("[INFO] 开始HF网络连接检查...")
    
    # 测试端点列表
    endpoints = [
        "https://huggingface.co/api/health",
        "https://huggingface.co/api/models",
        "https://huggingface.co/api/spaces",
        "https://huggingface.co/api/datasets"
    ]
    
    results = {}
    
    for endpoint in endpoints:
        print(f"[INFO] 测试连接: {endpoint}")
        try:
            start_time = time.time()
            response = requests.get(endpoint, timeout=10)
            end_time = time.time()
            
            if response.status_code == 200:
                duration = end_time - start_time
                results[endpoint] = {
                    'status': 'OK',
                    'duration': f"{duration:.2f}s",
                    'status_code': response.status_code
                }
                print(f"[SUCCESS] 连接成功 - {duration:.2f}s")
            else:
                results[endpoint] = {
                    'status': 'ERROR',
                    'status_code': response.status_code,
                    'error': f"HTTP {response.status_code}"
                }
                print(f"[ERROR] 连接失败 - HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            results[endpoint] = {
                'status': 'TIMEOUT',
                'error': '请求超时'
            }
            print(f"[ERROR] 连接超时")
            
        except requests.exceptions.ConnectionError:
            results[endpoint] = {
                'status': 'CONNECTION_ERROR',
                'error': '连接错误'
            }
            print(f"[ERROR] 连接错误")
            
        except Exception as e:
            results[endpoint] = {
                'status': 'OTHER_ERROR',
                'error': str(e)
            }
            print(f"[ERROR] 其他错误: {e}")
    
    # 汇总结果
    print("\n[SUMMARY] HF连接检查结果:")
    success_count = 0
    for endpoint, result in results.items():
        status = result['status']
        if status == 'OK':
            success_count += 1
            print(f"[✓] {endpoint} - {result['duration']}")
        else:
            print(f"[✗] {endpoint} - {result.get('error', '未知错误')}")
    
    print(f"\n[RESULT] 成功: {success_count}/{len(endpoints)}")
    
    # 判断网络状态
    if success_count == len(endpoints):
        print("[SUCCESS] HF Hub完全可访问")
        return True
    elif success_count >= 2:
        print("[WARNING] HF Hub部分可访问，建议稍后重试")
        return False
    else:
        print("[ERROR] HF Hub连接严重问题，需要检查网络")
        return False

if __name__ == "__main__":
    success = check_hf_connection()
    sys.exit(0 if success else 1)