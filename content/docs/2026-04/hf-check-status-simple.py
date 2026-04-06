import requests
import json
from datetime import datetime

print('HF API 状态检查开始...')
print(f'检查时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# 检查 API 端点状态
endpoints = {
    '主页': 'https://huggingface.co',
    '健康检查': 'https://huggingface.co/api/health',
    '模型列表': 'https://huggingface.co/api/models',
    '组织信息': 'https://huggingface.co/api/organizations/IKUN-LLM',
    '模型详情': 'https://huggingface.co/api/models/ikun-2.5B'
}

status_results = {}
for name, url in endpoints.items():
    try:
        response = requests.get(url, timeout=10)
        status = '正常' if response.status_code == 200 else f'异常 ({response.status_code})'
        status_results[name] = {'url': url, 'status': status, 'response_time': response.elapsed.total_seconds()}
        print(f'{name}: {status} - 响应时间: {response.elapsed.total_seconds():.2f}s')
    except Exception as e:
        status_results[name] = {'url': url, 'status': f'连接失败 ({str(e)})', 'response_time': 0}
        print(f'{name}: 连接失败 ({str(e)})')

print()
print('API状态汇总:')
successful = sum(1 for result in status_results.values() if '正常' in result['status'])
total = len(status_results)
print(f'正常端点: {successful}/{total} ({successful/total*100:.1f}%)')

print()
print('HF系统状态评估:')
if successful == total:
    print('HF API 完全正常，所有端点可用')
elif successful >= total * 0.8:
    print('HF API 基本正常，个别端点有问题')
else:
    print('HF API 问题较多，需要修复')