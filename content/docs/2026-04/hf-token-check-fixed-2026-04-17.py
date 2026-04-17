#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HF Token验证脚本 - 2026-04-17
验证HuggingFace Token有效性和组织访问权限
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from huggingface_hub import HfApi
    from huggingface_hub.utils import HfHubHTTPError
    import json
    print("SUCCESS: 成功导入huggingface_hub库")
except ImportError as e:
    print(f"ERROR: 导入失败: {e}")
    sys.exit(1)

def check_token_validity():
    """检查Token有效性"""
    print("\nCHECKING: 开始Token验证...")
    
    try:
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(__file__), 'hf-config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                token = config.get('hf_token', '')
        else:
            print("ERROR: 配置文件不存在")
            return False
            
        if token == "hf_[YOUR_HUGGINGFACE_TOKEN_HERE]" or token == "":
            print("ERROR: Token为空或使用占位符")
            return False
            
        # 验证Token
        api = HfApi(token=token)
        user_info = api.whoami()
        print(f"SUCCESS: HF Token有效，用户: {user_info['name']} ({user_info['type']})")
        print(f"   - 用户ID: {user_info['id']}")
        print(f"   - 空间配额: {user_info.get('diskSpace', 0)} MB")
        print(f"   - 付费状态: {'SUCCESS: 付费' if user_info.get('jobId', 0) > 0 else 'FREE: 免费'}")
        
        # 检查组织访问权限
        print(f"\nCHECKING: 检查组织访问权限...")
        try:
            orgs = api.list_orgs()
            org_names = [org.name for org in orgs]
            print(f"   - 可访问组织: {len(org_names)}个")
            
            if "IKUN-LLM" in org_names:
                print("SUCCESS: IKUN-LLM组织访问正常")
                
                # 检查组织下的模型
                try:
                    models = api.list_models(search="IKUN-LLM", limit=10)
                    ikun_models = [m for m in models if "IKUN-LLM" in m.id]
                    print(f"   - IKUN-LLM下模型数量: {len(ikun_models)}")
                    for model in ikun_models[:3]:  # 显示前3个
                        print(f"     - {model.id}")
                except Exception as e:
                    print(f"WARNING: 获取组织模型失败: {e}")
                    
            else:
                print("ERROR: 无法访问IKUN-LLM组织")
                return False
                
        except Exception as e:
            print(f"ERROR: 获取组织列表失败: {e}")
            return False
            
        return True
        
    except HfHubHTTPError as e:
        print(f"ERROR: HTTP错误: {e}")
        if "invalid token" in str(e).lower():
            print("   - Token已过期或无效")
        elif "rate limit" in str(e).lower():
            print("   - API调用频率超限")
        return False
    except Exception as e:
        print(f"ERROR: Token验证失败: {e}")
        return False

def main():
    """主函数"""
    print("STARTING: HF Token验证程序启动 - 2026-04-17")
    print("=" * 50)
    
    success = check_token_validity()
    
    print("\n" + "=" * 50)
    if success:
        print("SUCCESS: Token验证成功！系统运行正常")
        return 0
    else:
        print("FAILED: Token验证失败！需要检查配置")
        return 1

if __name__ == "__main__":
    sys.exit(main())