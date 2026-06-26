#!/usr/bin/env python3
"""
收集HF IKUN-LLM组织每日运营数据
"""

import os
import sys
from datetime import datetime
from huggingface_hub import HfApi

def collect_data():
    """收集运营数据"""
    print("[INFO] 开始收集HF IKUN-LLM运营数据...")
    
    # 读取Token
    token_file = os.path.expanduser('~/.cache/huggingface/token')
    if not os.path.exists(token_file):
        token_file = 'C:/Users/PC/.cache/huggingface/token'
    
    with open(token_file, 'r') as f:
        token = f.read().strip()
    
    api = HfApi(token=token)
    
    # 获取资产数据
    models = list(api.list_models(author="IKUN-LLM"))
    spaces = list(api.list_spaces(author="IKUN-LLM"))
    datasets = list(api.list_datasets(author="IKUN-LLM"))
    
    # 计算统计数据
    total_downloads = sum(getattr(m, 'downloads', 0) for m in models)
    total_likes = sum(getattr(s, 'likes', 0) for s in spaces)
    total_dataset_downloads = sum(getattr(d, 'downloads', 0) for d in datasets)
    
    # 详细数据
    model_data = []
    for m in models:
        model_data.append({
            'id': m.id,
            'downloads': getattr(m, 'downloads', 0),
            'likes': getattr(m, 'likes', 0),
            'last_modified': str(getattr(m, 'last_modified', 'N/A'))
        })
    
    space_data = []
    for s in spaces:
        space_data.append({
            'id': s.id,
            'likes': getattr(s, 'likes', 0),
            'updated_at': str(getattr(s, 'updated_at', 'N/A'))
        })
    
    dataset_data = []
    for d in datasets:
        dataset_data.append({
            'id': d.id,
            'downloads': getattr(d, 'downloads', 0),
            'likes': getattr(d, 'likes', 0)
        })
    
    # 打印结果
    print(f"[RESULT] 数据收集完成:")
    print(f"  模型数量: {len(models)}")
    print(f"  Spaces数量: {len(spaces)}")
    print(f"  数据集数量: {len(datasets)}")
    print(f"  总模型下载量: {total_downloads}")
    print(f"  总数据集下载量: {total_dataset_downloads}")
    print(f"  总点赞: {total_likes}")
    
    for m in model_data:
        print(f"  - {m['id']}: {m['downloads']} downloads")
    
    result = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M:%S'),
        'timezone': 'Asia/Shanghai',
        'assets': {
            'models': {
                'count': len(models),
                'total_downloads': total_downloads,
                'details': model_data
            },
            'spaces': {
                'count': len(spaces),
                'total_likes': total_likes,
                'details': space_data
            },
            'datasets': {
                'count': len(datasets),
                'total_downloads': total_dataset_downloads,
                'details': dataset_data
            }
        },
        'summary': {
            'total_downloads': total_downloads + total_dataset_downloads,
            'total_assets': len(models) + len(spaces) + len(datasets)
        }
    }
    
    return result

if __name__ == "__main__":
    data = collect_data()
    import json
    output_file = f"hf-daily-data-{data['date']}.json"
    output_path = os.path.join(os.path.expanduser('~/.openclaw/workspace/memory'), output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 数据已保存到: {output_path}")
