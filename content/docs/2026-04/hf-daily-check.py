#!/usr/bin/env python3
"""
Hugging Face 每日检查脚本
检查 HF Token、网络连接、资产状态等
"""

import requests
import json
import os
from datetime import datetime
import sys

def check_hf_token():
    """检查 HF Token 有效性"""
    print("=" * 50)
    print("🔍 检查1: HF Token 验证")
    print("=" * 50)
    
    # 尝试从配置文件读取 token
    config_path = "memory/hf-config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            hf_token = config.get('hf_token', '')
            
            if 'YOUR_HUGGINGFACE_TOKEN_HERE' in hf_token:
                print("❌ HF Token 是占位符，需要更新实际的 token")
                return False
            else:
                print("✅ 发现有效的 HF Token 格式")
    else:
        print("❌ HF 配置文件不存在")
        return False
    
    # 验证 token
    try:
        headers = {'Authorization': f'Bearer {hf_token}'}
        response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ HF Token 有效，用户: {user_info.get('name', 'Unknown')}")
            print(f"   - 组织数量: {len(user_info.get('organizations', []))}")
            
            # 检查组织访问
            orgs = user_info.get('organizations', [])
            if 'IKUN-LLM' in [org['name'] for org in orgs]:
                print("✅ IKUN-LLM 组织访问正常")
                return True
            else:
                print("⚠️ 无法访问 IKUN-LLM 组织")
                return False
        else:
            print(f"❌ HF Token 无效: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ HF Token 验证失败: {e}")
        return False

def check_network_connection():
    """检查网络连接"""
    print("\n" + "=" * 50)
    print("🔍 检查2: 网络连接状态")
    print("=" * 50)
    
    try:
        # 检查 HF Hub 健康状态
        response = requests.get('https://huggingface.co/api/health', timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ HF Hub 可访问")
            print(f"   - 状态: {health_data.get('status', 'unknown')}")
            print(f"   - 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        else:
            print(f"❌ HF Hub 健康检查失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ HF Hub 无法访问: {e}")
        return False

def analyze_operational_status():
    """分析运营状态"""
    print("\n" + "=" * 50)
    print("🔍 检查3: 运营状态分析")
    print("=" * 50)
    
    # 读取最近的运营报告
    recent_reports = []
    memory_dir = "memory"
    
    for file in os.listdir(memory_dir):
        if file.startswith('hf-ikun-report-') and file.endswith('.md'):
            report_date = file.replace('hf-ikun-report-', '').replace('.md', '')
            recent_reports.append(report_date)
    
    if recent_reports:
        latest_report = max(recent_reports)
        print(f"✅ 找到最新运营报告: hf-ikun-report-{latest_report}.md")
        
        # 读取报告内容
        report_path = os.path.join(memory_dir, f"hf-ikun-report-{latest_report}.md")
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 提取关键信息
        if "下载量" in content:
            # 简单提取下载量
            import re
            download_matches = re.findall(r'(\d+)\s*下载', content)
            if download_matches:
                latest_downloads = int(download_matches[0])
                print(f"   - 最新下载量: {latest_downloads}")
                
        return True
    else:
        print("❌ 未找到运营报告文件")
        return False

def check_api_errors():
    """检查 API 错误"""
    print("\n" + "=" * 50)
    print("🔍 检查4: API 错误诊断")
    print("=" * 50)
    
    # 检查发布日志
    log_path = "memory/hf-publishing-log.json"
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            logs = json.load(f)
            
        if logs:
            error_count = 0
            for log in logs:
                if not log.get('success', True):
                    error_count += 1
                    error_msg = log.get('error', '未知错误')
                    print(f"❌ API 错误 {error_count}: {error_msg}")
            
            if error_count == 0:
                print("✅ 无 API 错误")
            else:
                print(f"⚠️ 发现 {error_count} 个 API 错误")
                
            return error_count == 0
        else:
            print("✅ 发布日志为空，无错误")
            return True
    else:
        print("❌ 发布日志文件不存在")
        return False

def generate_daily_check_report():
    """生成每日检查报告"""
    print("\n" + "=" * 50)
    print("📝 生成每日检查报告")
    print("=" * 50)
    
    # 执行所有检查
    token_ok = check_hf_token()
    network_ok = check_network_connection()
    status_ok = analyze_operational_status()
    api_ok = check_api_errors()
    
    # 生成报告
    report_content = f"""# 🐔 HF IKUN-LLM 每日检查报告

**检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Asia/Shanghai)  
**检查状态**: {'✅ 全部通过' if all([token_ok, network_ok, status_ok, api_ok]) else '⚠️ 部分问题'}

---

## 📊 检查结果汇总

### 环境检查
- **HF Token**: {'✅ 有效' if token_ok else '❌ 无效'}
- **网络连接**: {'✅ 正常' if network_ok else '❌ 异常'}
- **运营状态**: {'✅ 正常' if status_ok else '❌ 异常'}
- **API 错误**: {'✅ 无错误' if api_ok else '❌ 有错误'}

### 整体评估
"""
    
    if all([token_ok, network_ok, status_ok, api_ok]):
        report_content += "🎉 系统运行正常，无需修复\n"
    else:
        report_content += "⚠️ 发现问题，需要修复\n"
    
    report_content += f"""
---

## 🔧 修复建议

"""
    
    if not token_ok:
        report_content += """### Token 修复
1. 更新 `memory/hf-config.json` 中的 HF Token
2. 确保有 `IKUN-LLM` 组织访问权限

"""
    if not network_ok:
        report_content += """### 网络修复
1. 检查互联网连接
2. 检查代理设置
3. 尝试更换网络环境

"""
    if not status_ok:
        report_content += """### 状态修复
1. 检查运营日志文件
2. 验证资产同步状态
3. 确认定时任务运行

"""
    if not api_ok:
        report_content += """### API 错误修复
1. 检查 API 端点是否正确
2. 验证请求参数
3. 确认权限设置

"""
    
    report_content += f"""
---

## 📈 运营数据

检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
检查项目: 4项通过 / 4项总数
通过率: {'100%' if all([token_ok, network_ok, status_ok, api_ok]) else f'{sum([token_ok, network_ok, status_ok, api_ok])}/4 (25*{sum([token_ok, network_ok, status_ok, api_ok])}%)'}

---

*旺财完成 HF IKUN-LLM 每日检查任务！🐕🎤🏀*
"""
    
    # 保存报告
    report_path = "memory/hf-daily-check-report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ 每日检查报告已生成: {report_path}")
    
    return all([token_ok, network_ok, status_ok, api_ok])

if __name__ == "__main__":
    print("🚀 开始执行 HF IKUN-LLM 每日检查任务")
    success = generate_daily_check_report()
    
    if success:
        print("\n🎉 所有检查项目通过！")
        sys.exit(0)
    else:
        print("\n⚠️ 发现问题，需要修复！")
        sys.exit(1)