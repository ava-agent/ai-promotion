import requests
import json

print('HF Token 验证开始...')
print()

# 尝试获取环境变量或配置文件中的 token
token_file = 'memory/hf-token.txt'
api_token = None

# 尝试从文件读取 token
try:
    with open(token_file, 'r') as f:
        api_token = f.read().strip()
        print(f'从文件读取到token: {api_token[:20]}...' if api_token else '文件中未找到token')
except:
    print('未找到token文件')

# 如果没有从文件读取，尝试其他方式
if not api_token:
    print('尝试从环境变量获取token...')
    import os
    api_token = os.environ.get('HF_TOKEN')
    if api_token:
        print(f'从环境变量获取到token: {api_token[:20]}...')
    else:
        print('未找到环境变量中的token')

# 如果还是没有token，询问用户
if not api_token:
    print('错误: 未找到有效的HF Token')
    print('请确保以下之一存在:')
    print(f'1. 文件: {token_file}')
    print('2. 环境变量: HF_TOKEN')
    exit(1)

print()
print('开始验证token有效性...')
print()

# 验证token
try:
    headers = {
        'Authorization': f'Bearer {api_token}',
        'User-Agent': 'OpenClaw-HF-Monitor'
    }
    
    # 获取用户信息
    response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
    
    if response.status_code == 200:
        user_info = response.json()
        print(f'✅ Token有效')
        print(f'用户名: {user_info.get("name", "未知")}')
        print(f'组织: {user_info.get("organization", "无")}')
        print(f'类型: {user_info.get("type", "未知")}')
        
        # 检查组织访问权限
        orgs = user_info.get('organizations', [])
        if 'IKUN-LLM' in orgs:
            print('✅ IKUN-LLM组织访问权限正常')
        else:
            print('⚠️ 无法访问IKUN-LLM组织')
            
        return True
    else:
        print(f'❌ Token无效，状态码: {response.status_code}')
        print(f'错误信息: {response.text}')
        return False
        
except Exception as e:
    print(f'❌ Token验证失败: {str(e)}')
    return False