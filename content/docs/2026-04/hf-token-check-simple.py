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
    print("[INFO] 开始HF Token验证...")
    
    # 尝试从环境变量读取Token
    token = os.environ.get('HF_TOKEN')
    if not token:
        # 尝试从文件读取Token
        token_file = os.path.expanduser('~/.cache/huggingface/token')
        if not os.path.exists(token_file):
            token_file = 'C:/Users/PC/.cache/huggingface/token'
        
        if os.path.exists(token_file):
            try:
                with open(token_file, 'r') as f:
                    token = f.read().strip()
                print("[INFO] 从文件读取到HF Token")
            except Exception as e:
                print(f"[ERROR] 读取Token文件失败: {e}")
        else:
            print("[ERROR] 未找到HF Token文件")
            return False
    
    if not token:
        print("[ERROR] 未找到有效的HF Token")
        return False
    
    print("[INFO] 找到HF Token")
    
    try:
        # 创建API实例
        api = HfApi(token=token)
        
        # 验证Token有效性
        user_info = api.whoami()
        print(f"[SUCCESS] HF Token有效，用户: {user_info['name']}")
        print(f"   用户ID: {user_info['id']}")
        print(f"   空间数量: {user_info.get('spaceFans', 0)}")
        print(f"   模型数量: {user_info.get('modelFans', 0)}")
        
        # 检查组织访问
        try:
            orgs = api.list_organization_members("IKUN-LLM")
            print("[SUCCESS] IKUN-LLM组织访问正常")
        except Exception as e:
            print(f"[INFO] 无法直接访问IKUN-LLM组织，尝试其他方式: {e}")
            # 检查用户拥有的模型
            try:
                models = api.list_models()
                model_names = [model.id for model in models]
                print(f"[INFO] 用户拥有模型: {model_names}")
                
                # 检查spaces
                spaces = api.list_spaces()
                space_names = [space.id for space in spaces]
                print(f"[INFO] 用户拥有Spaces: {space_names}")
                
                return True
            except Exception as e2:
                print(f"[ERROR] 获取资产信息失败: {e2}")
                return False
            
            print(f"   模型数量: {len(list(models))}")
            print(f"   Spaces数量: {len(list(spaces))}")
            print(f"   数据集数量: {len(list(datasets))}")
            
            return True
        else:
            print("[WARNING] 无法访问IKUN-LLM组织")
            return False
            
    except HfHubHTTPError as e:
        print(f"[ERROR] HF API错误: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 验证失败: {e}")
        return False

if __name__ == "__main__":
    success = check_hf_token()
    sys.exit(0 if success else 1)