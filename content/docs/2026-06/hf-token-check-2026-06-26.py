from huggingface_hub import HfApi
import os
import json

try:
    api = HfApi()
    user_info = api.whoami()
    print("[OK] HF Token valid, user: {}".format(user_info['name']))
    
    # Print available keys for debugging
    print("[INFO] Available keys: {}".format(list(user_info.keys())))
    
    # Check for id in different possible keys
    user_id = user_info.get('id') or user_info.get('_id') or 'unknown'
    print("[INFO] User ID: {}".format(user_id))
    
    # 检查组织访问 - from user_info
    if 'orgs' in user_info:
        org_names = [org.get('name') for org in user_info['orgs']] if isinstance(user_info['orgs'], list) else []
        print("[INFO] User orgs: {}".format(org_names))
        if "IKUN-LLM" in org_names:
            print("[OK] IKUN-LLM organization access OK")
        else:
            print("[WARN] IKUN-LLM not found in user orgs")
            # Try to list models in IKUN-LLM to check access indirectly
            try:
                models = list(api.list_models(author="IKUN-LLM"))
                print("[OK] Can list models in IKUN-LLM, access OK. Found {} models".format(len(models)))
                for model in models:
                    print("  - {}".format(model.id))
            except Exception as access_err:
                print("[ERROR] Cannot access IKUN-LLM: {}".format(access_err))
    else:
        print("[WARN] No orgs info in user_info")
        
except Exception as e:
    print("[ERROR] HF Token invalid: {}".format(e))
    import traceback
    traceback.print_exc()
