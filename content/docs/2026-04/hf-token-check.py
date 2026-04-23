#!/usr/bin/env python3
"""
Hugging Face Token 验证脚本
用于验证HF Token的有效性和权限
"""

import os
import sys
from huggingface_hub import HfApi
from huggingface_hub.utils import HfHubHTTPError

def check_hf_token():
    """检查HF Token状态"""
    print("🔍 开始HF Token验证...")
    
    # 尝试从不同位置读取Token
    token_sources = [
        os.environ.get('HF_TOKEN'),
        os.path.expanduser('~/.cache/huggingface/token'),
        'C:/Users/PC/.cache/huggingface/token'
    ]
    
    token = None
    for source in token_sources:
        if source and os.path.exists(source):
            try:
                with open(source, 'r') as f:
                    token = f.read().strip()
                break
            except Exception as e:
                print(f"❌ 读取Token文件失败: {e}")
    
    if not token:
        print("❌ 未找到有效的HF Token")
        return False
    
    print("✅ 找到HF Token")
    
    try:
        # 创建API实例
        api = HfApi(token=token)
        
        # 验证Token有效性
        user_info = api.whoami()
        print(f"✅ HF Token有效，用户: {user_info['name']}")
        print(f"   用户ID: {user_info['id']}")
        print(f"   空间数量: {user_info['spaceFans']}")
        print(f"   模型数量: {user_info['modelFans']}")
        
        # 检查组织访问
        orgs = api.list_orgs()
        org_names = [org.name for org in orgs]
        print(f"📋 可访问组织: {org_names}")
        
        if "IKUN-LLM" in org_names:
            print("✅ IKUN-LLM组织访问正常")
            
            # 检查组织下的资产
            print("\n📊 IKUN-LLM组织资产检查:")
            models = api.list_models(filter="IKUN-LLM")
            spaces = api.list_spaces(filter="IKUN-LLM")
            datasets = api.list_datasets(filter="IKUN-LLM")
            
            print(f"   模型数量: {len(list(models))}")
            print(f"   Spaces数量: {len(list(spaces))}")
            print(f"   数据集数量: {len(list(datasets))}")
            
            return True
        else:
            print("⚠️ 无法访问IKUN-LLM组织")
            return False
            
    except HfHubHTTPError as e:
        print(f"❌ HF API错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    success = check_hf_token()
    sys.exit(0 if success else 1)