#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HF网络连接检查脚本 - 2026-04-17
检查HuggingFace Hub网络连接和API响应状态
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

def check_hf_connectivity():
    """检查HF Hub连接状态"""
    print("🌐 开始HF Hub连接检查...")
    
    endpoints = [
        ("健康检查", "https://huggingface.co/api/health"),
        ("组织搜索", "https://huggingface.co/api/organizations/search?q=ikun"),
        ("模型搜索", "https://huggingface.co/api/models/search?q=ikun"),
        ("通用API", "https://huggingface.co/api/models")
    ]
    
    results = []
    
    for name, url in endpoints:
        try:
            print(f"   🔍 检查{name}: {url}")
            start_time = time.time()
            
            response = requests.get(url, timeout=10, allow_redirects=True)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                print(f"   ✅ {name} - 成功 (响应时间: {elapsed:.2f}s)")
                
                if name == "健康检查":
                    try:
                        health_data = response.json()
                        print(f"     - Hub状态: {health_data.get('hub_status', 'unknown')}")
                        print(f"     - 服务状态: {health_data.get('service_status', 'unknown')}")
                    except:
                        print("     - 响应数据解析失败")
                        
                results.append((name, True, elapsed))
            else:
                print(f"   ❌ {name} - 失败 (HTTP {response.status_code})")
                results.append((name, False, elapsed))
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ {name} - 超时")
            results.append((name, False, 0))
        except requests.exceptions.ConnectionError:
            print(f"   🔌 {name} - 连接错误")
            results.append((name, False, 0))
        except Exception as e:
            print(f"   💥 {name} - 错误: {e}")
            results.append((name, False, 0))
    
    return results

def check_upload_capability():
    """检查上传功能"""
    print("\n📤 检查上传功能...")
    
    # 模拟上传测试（不实际上传）
    upload_endpoint = "https://huggingface.co/api/models"
    
    try:
        # 检查是否可以创建模型（通过OPTIONS请求）
        response = requests.options(upload_endpoint, timeout=10)
        
        if response.status_code in [200, 405]:  # 200或405 Method Not Allowed都是正常的
            print("✅ 上传接口可访问")
            return True
        else:
            print(f"❌ 上传接口异常 (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ 上传功能检查失败: {e}")
        return False

def check_rate_limits():
    """检查API调用限制"""
    print("\n📊 检查API调用限制...")
    
    try:
        # 检查Rate Limit头信息
        response = requests.get("https://huggingface.co/api/models", timeout=10)
        
        if response.status_code == 200:
            headers = response.headers
            rate_limit = headers.get('x-ratelimit-limit', 'unknown')
            rate_remaining = headers.get('x-ratelimit-remaining', 'unknown')
            rate_reset = headers.get('x-ratelimit-reset', 'unknown')
            
            print(f"   - API限制: {rate_limit}")
            print(f"   - 剩余次数: {rate_remaining}")
            
            if rate_reset != 'unknown':
                reset_time = int(rate_reset)
                reset_dt = datetime.fromtimestamp(reset_time)
                print(f"   - 重置时间: {reset_dt}")
                
            # 检查是否接近限制
            if rate_remaining != 'unknown' and int(rate_remaining) < 10:
                print("   ⚠️ 警告: API调用次数接近限制")
                return False
            else:
                print("   ✅ API调用次数充足")
                return True
        else:
            print(f"❌ 无法获取Rate Limit信息 (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Rate Limit检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 HF网络连接检查程序启动 - 2026-04-17")
    print("=" * 50)
    
    # 检查基本连接
    connectivity_results = check_hf_connectivity()
    
    # 检查上传功能
    upload_status = check_upload_capability()
    
    # 检查API限制
    rate_status = check_rate_limits()
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📋 检查结果汇总:")
    
    success_count = sum(1 for _, success, _ in connectivity_results if success)
    total_count = len(connectivity_results)
    
    print(f"   - API连接: {success_count}/{total_count}")
    print(f"   - 上传功能: {'✅ 正常' if upload_status else '❌ 异常'}")
    print(f"   - API限制: {'✅ 正常' if rate_status else '❌ 异常'}")
    
    # 判断整体状态
    overall_success = (success_count == total_count and 
                      upload_status and 
                      rate_status)
    
    if overall_success:
        print("\n🎉 网络连接检查全部通过！")
        return 0
    else:
        print("\n💥 部分检查项目失败，需要修复")
        return 1

if __name__ == "__main__":
    sys.exit(main())