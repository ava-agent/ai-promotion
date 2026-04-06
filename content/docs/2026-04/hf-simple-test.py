#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HF 简单连接测试脚本 - 避免编码问题
"""

import requests
import json
import os
from datetime import datetime

def test_basic_connectivity():
    """测试基本连接"""
    print("测试 HF 基本连接...")
    
    try:
        response = requests.get('https://huggingface.co', timeout=10)
        if response.status_code == 200:
            print("HF 主页访问正常")
            return True
        else:
            print(f"HF 主页访问异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"HF 主页无法访问: {e}")
        return False

def test_hf_health():
    """测试 HF 健康检查"""
    print("\n测试 HF 健康检查...")
    
    try:
        response = requests.get('https://huggingface.co/api/health', timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("HF 健康检查正常")
            print(f"状态: {health_data.get('status', 'unknown')}")
            return True
        else:
            print(f"HF 健康检查异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"HF 健康检查失败: {e}")
        return False

def create_simple_report():
    """创建简单报告"""
    print("\n" + "=" * 50)
    print("生成测试报告")
    print("=" * 50)
    
    # 执行测试
    basic_ok = test_basic_connectivity()
    health_ok = test_hf_health()
    
    report_content = f"""# HF 连接测试报告

**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Asia/Shanghai)

---

## 测试结果

### 基础连接
- **HF 主页访问**: {'正常' if basic_ok else '异常'}

### 健康检查
- **HF API 健康状态**: {'正常' if health_ok else '异常'}

---

## 整体评估

测试状态: {'通过' if all([basic_ok, health_ok]) else '部分失败'}

---

## 建议

"""
    
    if not basic_ok:
        report_content += """### 基础连接修复
1. 检查网络连接
2. 检查代理设置
3. 检查防火墙

"""
    
    if not health_ok:
        report_content += """### API 修复
1. 检查 HF 服务状态
2. 验证网络延迟
3. 检查 API 端点

"""
    
    report_content += f"""
---

## 测试详情

- 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 测试项目: 2项
- 通过项目: {sum([basic_ok, health_ok])}项
- 通过率: {sum([basic_ok, health_ok])}/2 ({sum([basic_ok, health_ok])*50}%)

---

*旺财完成 HF 连接测试！*
"""
    
    # 保存报告
    report_path = "memory/hf-simple-test-report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"测试报告已保存: {report_path}")
    
    return all([basic_ok, health_ok])

if __name__ == "__main__":
    print("开始 HF 连接测试...")
    success = create_simple_report()
    
    if success:
        print("\n所有测试通过！")
    else:
        print("\n发现测试问题，需要修复！")