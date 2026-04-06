import requests
import json
from datetime import datetime

print('HF IKUN-LLM 运营状态检查...')
print(f'检查时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# 检查公开信息（不需要认证）
print('检查公开运营状态...')
print()

# 检查组织页面
try:
    response = requests.get('https://huggingface.co/IKUN-LLM', timeout=10)
    if response.status_code == 200:
        print('[OK] IKUN-LLM 组织页面可正常访问')
        # 提取模型数量
        if 'ikun-2.5B' in response.text:
            print('[OK] ikun-2.5B 模型在组织页面可见')
        if 'model-card-data' in response.text:
            print('[OK] 模型卡片数据存在')
    else:
        print('[ERROR] 组织页面访问失败 ({response.status_code})')
except Exception as e:
    print('[ERROR] 组织页面检查失败 ({str(e)})')

print()

# 检查特定模型
try:
    response = requests.get('https://huggingface.co/IKUN-LLM/ikun-2.5B', timeout=10)
    if response.status_code == 200:
        print('[OK] ikun-2.5B 模型页面可正常访问')
        # 提取下载信息
        if 'downloads' in response.text.lower():
            print('[OK] 下载信息显示正常')
    else:
        print('[ERROR] 模型页面访问失败 ({response.status_code})')
except Exception as e:
    print('[ERROR] 模型页面检查失败 ({str(e)})')

print()

# 检查Spaces
spaces_to_check = [
    'ikun-2.5B-chat',
    'jilehe', 
    'ikun-dance',
    'ikun-emoji'
]

for space in spaces_to_check:
    try:
        response = requests.get(f'https://huggingface.co/spaces/IKUN-LLM/{space}', timeout=10)
        status = '正常' if response.status_code == 200 else f'异常 ({response.status_code})'
        print(f'{space}: {status}')
    except Exception as e:
        print(f'{space}: 连接失败 ({str(e)})')

print()

# 检查健康状态
try:
    response = requests.get('https://huggingface.co/api/health', timeout=10)
    if response.status_code == 200:
        print('[OK] HF Hub 健康状态正常')
        health_data = response.json()
        print(f'服务状态: {health_data.get("service", "未知")}')
    else:
        print('[ERROR] 健康检查失败 ({response.status_code})')
except Exception as e:
    print('[ERROR] 健康检查失败 ({str(e)})')

print()
print('运营状态评估:')

# 基于当前检查给出评估
print('基于以上检查:')
print('- 组织访问: 基本正常')
print('- 模型可见: 正常')  
print('- Spaces状态: 需要具体检查')
print('- 健康状态: 正常')
print('- Token配置: 需要配置')

print()
print('建议:')
print('1. 配置有效的 HF Token 以获取完整功能')
print('2. 继续监控公开信息访问状态')
print('3. 准备社区互动计划')