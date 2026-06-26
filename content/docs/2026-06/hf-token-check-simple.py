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
        
        # 检查组织访问 - 先列出用户所属的组织
        try:
            orgs = api.list_orgs()
            org_names = [org.name for org in orgs]
            print(f"[INFO] 用户所属组织: {org_names}")
            
            if "IKUN-LLM" in org_names:
                print("[SUCCESS] 用户已加入IKUN-LLM组织，访问权限正常")
                
                # 尝试列出组织内模型确认权限
                try:
                    models = list(api.list_models(author="IKUN-LLM"))
                    spaces = list(api.list_spaces(author="IKUN-LLM"))
                    datasets = list(api.list_datasets(author="IKUN-LLM"))
                    print(f"[INFO] IKUN-LLN组织资产:")
                    print(f"   模型数量: {len(models)}")
                    print(f"   Spaces数量: {len(spaces)}")
                    print(f"   数据集数量: {len(datasets)}")
                    for model in models:
                        print(f"   - 模型: {model.id}")
                    for space in spaces:
                        print(f"   - Space: {space.id}")
                    for dataset in datasets:
                        print(f"   - 数据集: {dataset.id}")
                except Exception as e:
                    print(f"[WARNING] 获取组织资产信息时遇到问题: {e}")
                
                return True
            else:
                print("[WARNING] 用户不在IKUN-LLM组织中")
                return False
                
        except Exception as e:
            print(f"[ERROR] 列出组织信息失败: {e}")
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