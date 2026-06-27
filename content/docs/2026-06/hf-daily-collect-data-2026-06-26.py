#!/usr/bin/env python3
"""
HF Daily Data Collection for IKUN-LLM Organization
Collects current statistics for models, spaces, datasets
"""

from huggingface_hub import HfApi
import json
from datetime import datetime

def collect_organization_data():
    api = HfApi()
    org_name = "IKUN-LLM"
    
    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "organization": org_name,
        "models": [],
        "spaces": [],
        "datasets": [],
        "summary": {
            "total_models": 0,
            "total_spaces": 0,
            "total_datasets": 0,
            "total_downloads": 0,
            "total_likes": 0
        }
    }
    
    # Collect models
    try:
        models = list(api.list_models(author=org_name))
        data["summary"]["total_models"] = len(models)
        
        for model in models:
            model_info = {
                "id": model.id,
                "downloads": model.downloads,
                "likes": model.likes,
                "tags": model.tags,
                "pipeline_tag": getattr(model, 'pipeline_tag', None)
            }
            data["models"].append(model_info)
            data["summary"]["total_downloads"] += model.downloads
            data["summary"]["total_likes"] += model.likes
            
        print(f"[OK] Collected {len(models)} models")
    except Exception as e:
        print(f"[ERROR] Failed to collect models: {e}")
    
    # Collect datasets
    try:
        datasets = list(api.list_datasets(author=org_name))
        data["summary"]["total_datasets"] = len(datasets)
        
        for dataset in datasets:
            dataset_info = {
                "id": dataset.id,
                "downloads": dataset.downloads,
                "likes": dataset.likes,
                "tags": dataset.tags
            }
            data["datasets"].append(dataset_info)
            data["summary"]["total_downloads"] += dataset.downloads
            data["summary"]["total_likes"] += dataset.likes
            
        print(f"[OK] Collected {len(datasets)} datasets")
    except Exception as e:
        print(f"[ERROR] Failed to collect datasets: {e}")
    
    # Collect spaces - need different approach
    try:
        # Use http request since HfApi doesn't have direct list_spaces for author
        import requests
        url = f"https://huggingface.co/api/orgs/{org_name}/spaces"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            spaces_data = response.json()
            data["summary"]["total_spaces"] = len(spaces_data)
            
            for space in spaces_data:
                space_info = {
                    "id": f"{org_name}/{space['name']}",
                    "name": space['name'],
                    "likes": space.get('likes', 0),
                    "status": space.get('status', 'unknown')
                }
                data["spaces"].append(space_info)
                data["summary"]["total_likes"] += space_info["likes"]
                
            print(f"[OK] Collected {len(spaces_data)} spaces")
        else:
            print(f"[WARN] Failed to get spaces, status: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Failed to collect spaces: {e}")
    
    return data

def main():
    print("[START] Collecting HF daily data...")
    
    data = collect_organization_data()
    
    # Print summary
    print("\n[SUMMARY]")
    print(f"  Models: {data['summary']['total_models']}")
    print(f"  Datasets: {data['summary']['total_datasets']}")
    print(f"  Spaces: {data['summary']['total_spaces']}")
    print(f"  Total downloads: {data['summary']['total_downloads']}")
    print(f"  Total likes: {data['summary']['total_likes']}")
    
    # Save to file
    output_file = f"memory/hf-daily-data-{data['date']}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Data saved to {output_file}")
    return data

if __name__ == "__main__":
    main()
