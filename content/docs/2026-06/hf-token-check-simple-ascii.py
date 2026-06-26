#!/usr/bin/env python3
"""
Hugging Face Token 验证脚本 - ASCII 版本
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
    else:
        print("[INFO] 从环境变量读取到HF Token")
    
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
        
        # 获取用户 organizations
        orgs = user_info.get('organizations', [])
        org_names = [org.get('name', '') for org in orgs] if isinstance(orgs, list) else []
        print(f"[INFO] 用户所属组织: {org_names}")
        
        has_ikun = False
        if "IKUN-LLM" in org_names or any("IKUN-LLM" in name for name in org_names):
            has_ikun = True
        
        # 尝试列出组织内模型确认权限
        print("[INFO] 尝试获取IKUN-LLM组织资产...")
        try:
            models = list(api.list_models(author="IKUN-LLM"))
            spaces = list(api.list_spaces(author="IKUN-LLM"))
            datasets = list(api.list_datasets(author="IKUN-LLM"))
            print(f"[INFO] IKUN-LLM组织资产:")
            print(f"   模型数量: {len(models)}")
            print(f"   Spaces数量: {len(spaces)}")
            print(f"   数据集数量: {len(datasets)}")
            for model in models:
                print(f"   - 模型: {model.id} (下载: {model.downloads})")
            for space in spaces:
                print(f"   - Space: {space.id} (点赞: {space.likes})")
            for dataset in datasets:
                print(f"   - 数据集: {dataset.id} (下载: {dataset.downloads})")
            
            if len(models) + len(spaces) + len(datasets) > 0:
                print("[SUCCESS] IKUN-LLM组织访问权限正常")
                return True
            else:
                print("[WARNING] 组织资产为空或无法读取")
                return has_ikun
            
        except Exception as e:
            print(f"[ERROR] 无法访问IKUN-LLM组织资产: {e}")
            print("[INFO] 需要检查用户组织成员权限")
            return False
            
    except HfHubHTTPError as e:
        print(f"[ERROR] HF API错误: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_hf_token()
    sys.exit(0 if success else 1)
