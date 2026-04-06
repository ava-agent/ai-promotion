#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HF 网络诊断脚本 - 深度分析 HF API 问题
"""

import requests
import json
import os
from datetime import datetime
import time

def test_hf_endpoints():
    """测试各种 HF API 端点"""
    print("HF API 端点诊断...")
    
    endpoints = {
        '主页': 'https://huggingface.co',
        '健康检查': 'https://huggingface.co/api/health',
        '模型列表': 'https://huggingface.co/api/models',
        '空间列表': 'https://huggingface.co/api/spaces',
        '数据集列表': 'https://huggingface.co/api/datasets',
        '组织信息': 'https://huggingface.co/IKUN-LLM',
        '模型详情': 'https://huggingface.co/IKUN-LLM/ikun-2.5B',
        '空间详情': 'https://huggingface.co/spaces/IKUN-LLM/ikun-2.5B-chat'
    }
    
    results = {}
    
    for name, url in endpoints.items():
        print(f"\n测试 {name}: {url}")
        try:
            start_time = time.time()
            response = requests.get(url, timeout=15)
            elapsed = time.time() - start_time
            
            print(f"  状态码: {response.status_code}")
            print(f"  响应时间: {elapsed:.2f}秒")
            
            if response.status_code == 200:
                # 检查内容长度
                content_length = len(response.content)
                print(f"  内容长度: {content_length} 字节")
                results[name] = {'status': 'ok', 'time': elapsed, 'size': content_length}
            else:
                print(f"  错误: {response.text[:200]}")
                results[name] = {'status': 'error', 'code': response.status_code}
                
        except requests.exceptions.Timeout:
            print("  超时")
            results[name] = {'status': 'timeout'}
        except requests.exceptions.ConnectionError:
            print("  连接错误")
            results[name] = {'status': 'connection_error'}
        except Exception as e:
            print(f"  异常: {e}")
            results[name] = {'status': 'exception', 'error': str(e)}
    
    return results

def diagnose_api_issues():
    """诊断 API 问题"""
    print("\n" + "=" * 60)
    print("API 问题诊断")
    print("=" * 60)
    
    # 测试端点
    results = test_hf_endpoints()
    
    # 分析结果
    working_endpoints = []
    problematic_endpoints = []
    
    for name, result in results.items():
        if result.get('status') == 'ok':
            working_endpoints.append(name)
        else:
            problematic_endpoints.append((name, result))
    
    print(f"\n诊断结果:")
    print(f"正常端点: {len(working_endpoints)}个")
    print(f"问题端点: {len(problematic_endpoints)}个")
    
    if problematic_endpoints:
        print("\n问题端点详情:")
        for name, result in problematic_endpoints:
            status = result.get('status', 'unknown')
            if status == 'timeout':
                print(f"  {name}: 超时")
            elif status == 'connection_error':
                print(f"  {name}: 连接错误")
            elif status == 'exception':
                error = result.get('error', '未知错误')
                print(f"  {name}: 异常 - {error}")
            else:
                print(f"  {name}: 状态码 {result.get('code', 'unknown')}")
    
    return results

def create_diagnosis_report():
    """创建诊断报告"""
    print("\n" + "=" * 60)
    print("生成诊断报告")
    print("=" * 60)
    
    # 执行诊断
    results = diagnose_api_issues()
    
    # 分析结果
    working_count = sum(1 for r in results.values() if r.get('status') == 'ok')
    total_count = len(results)
    
    report_content = f"""# HF API 诊断报告

**诊断时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Asia/Shanghai)

---

## 诊断结果

### 总体状况
- **正常端点**: {working_count}/{total_count} ({working_count/total_count*100:.1f}%)
- **问题端点**: {total_count - working_count}/{total_count} ({(total_count - working_count)/total_count*100:.1f}%)

### 端点状态详情
"""
    
    for name, result in results.items():
        status = result.get('status', 'unknown')
        if status == 'ok':
            status_str = "正常"
            time_info = result.get('time', 0)
            size_info = result.get('size', 0)
            detail = f"响应时间: {time_info:.2f}s, 大小: {size_info}字节"
        elif status == 'timeout':
            status_str = "超时"
            detail = ""
        elif status == 'connection_error':
            status_str = "连接错误"
            detail = ""
        else:
            status_str = f"错误({result.get('code', 'unknown')})"
            detail = result.get('error', '')[:100]
        
        report_content += f"- **{name}**: {status_str}"
        if detail:
            report_content += f" - {detail}"
        report_content += "\n"
    
    report_content += f"""

---

## 问题分析

### 主要问题类型
"""
    
    error_types = {}
    for result in results.values():
        status = result.get('status', 'unknown')
        if status != 'ok':
            error_types[status] = error_types.get(status, 0) + 1
    
    for error_type, count in error_types.items():
        report_content += f"- **{error_type}**: {count}个端点\n"
    
    report_content += f"""

### 修复建议
"""
    
    if 'timeout' in error_types:
        report_content += """**超时问题**:
1. 检查网络延迟
2. 增加 API 请求超时时间
3. 检查服务器负载

"""
    
    if 'connection_error' in error_types:
        report_content += """**连接错误**:
1. 检查网络连接
2. 检查代理设置
3. 检查防火墙配置

"""
    
    if 'exception' in error_types:
        report_content += """**异常错误**:
1. 检查 API 版本兼容性
2. 验证请求参数
3. 检查 API 访问权限

"""
    
    report_content += f"""

---

## 测试详情

- 诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 测试端点: {total_count}个
- 正常端点: {working_count}个
- 健康率: {working_count/total_count*100:.1f}%

---

*旺财完成 HF API 诊断！*
"""
    
    # 保存报告
    report_path = "memory/hf-api-diagnosis-report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n诊断报告已保存: {report_path}")
    
    return working_count >= total_count * 0.5  # 50% 以上正常就算成功

if __name__ == "__main__":
    print("开始 HF API 诊断...")
    success = create_diagnosis_report()
    
    if success:
        print("\n诊断完成：HF API 基本可用")
    else:
        print("\n诊断完成：HF API 存在较多问题")