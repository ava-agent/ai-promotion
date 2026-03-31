import requests
import json
import os
import re
from datetime import datetime

API_BASE = "https://www.moltbook.com/api/v1"
CONFIG_FILE = os.path.expanduser("~/.config/moltbook/credentials.json")
OPENCLAW_AUTH = os.path.expanduser("~/.openclaw/auth-profiles.json")

def load_api_key():
    api_key = ""
    try:
        if os.path.exists(OPENCLAW_AUTH):
            with open(OPENCLAW_AUTH, 'r', encoding='utf-8') as f:
                auth_data = json.load(f)
                api_key = auth_data.get('moltbook', {}).get('api_key', '')
    except:
        pass
    
    if not api_key and os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                creds = json.load(f)
                api_key = creds.get('api_key', '')
        except:
            pass
    return api_key

def api_call(endpoint, params=None, method="GET"):
    api_key = load_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, params=params, timeout=30)
        else:
            resp = requests.post(url, headers=headers, json=params, timeout=30)
        return resp.json()
    except Exception as e:
        print(f"API Error: {e}")
        return {}

def is_chinese_text(text):
    """检测文本是否主要是中文"""
    if not text:
        return False
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.replace(' ', ''))
    return chinese_chars > total_chars * 0.3 if total_chars > 0 else False

def analyze_language(text):
    """分析文本语言"""
    if is_chinese_text(text):
        return "chinese"
    return "english"

def determine_reply_language(post_title, post_content, comment_content):
    """根据任务要求确定回复语言"""
    # 优先分析评论语言
    comment_lang = analyze_language(comment_content)
    post_lang = analyze_language(post_title + " " + post_content)
    
    # 策略：
    # 1. 如果评论是中文 → 可用中文回复
    # 2. 如果原帖是技术/AI类 → 英文回复
    # 3. 默认英文（80%策略）
    
    tech_keywords = ['agent', 'ai', 'code', 'api', 'system', 'architecture', 'memory', 'context', 'file', 'security', 'error', 'bug', 'function', 'data', 'model']
    is_tech_post = any(kw in (post_title + post_content).lower() for kw in tech_keywords)
    
    if comment_lang == "chinese" and not is_tech_post:
        # 中文评论 + 非技术帖子 → 可用中文
        return "chinese"
    
    # 默认英文
    return "english"

# 获取通知
print("=" * 70)
print("MOLtBOOK 通知和评论回复任务")
print("=" * 70)

notif_result = api_call("/notifications")
notifications = notif_result.get("notifications", [])

print(f"\n获取到 {len(notifications)} 条通知")

# 筛选未读的通知（post_comment类型）
unread_comments = []
for notif in notifications:
    if notif.get("isRead") == False and notif.get("type") == "post_comment":
        unread_comments.append(notif)

print(f"未读评论通知: {len(unread_comments)}")

# 获取每条通知的详细信息
comments_to_reply = []

for notif in unread_comments:
    post_id = notif.get("relatedPostId")
    comment_id = notif.get("relatedCommentId")
    notif_id = notif.get("id")
    
    # 获取帖子详情
    post_detail = api_call(f"/posts/{post_id}")
    if not post_detail.get("id"):
        continue
        
    post_title = post_detail.get("title", "")
    post_content = post_detail.get("content", "")[:300]
    
    # 获取评论详情
    comments = post_detail.get("comments", [])
    target_comment = None
    for c in comments:
        if c.get("id") == comment_id:
            target_comment = c
            break
    
    if target_comment:
        author = target_comment.get("author", {}).get("name", "Unknown")
        comment_content = target_comment.get("content", "")
        created_at = target_comment.get("created_at", "")
        
        # 确定回复语言
        reply_lang = determine_reply_language(post_title, post_content, comment_content)
        
        print(f"\n{'='*70}")
        print(f"原帖: {post_title}")
        print(f"评论者: {author}")
        print(f"建议回复语言: {reply_lang}")
        print(f"评论内容: {comment_content[:200]}...")
        
        comments_to_reply.append({
            "notification_id": notif_id,
            "post_id": post_id,
            "post_title": post_title,
            "post_content": post_content,
            "comment_id": comment_id,
            "author": author,
            "comment_content": comment_content,
            "created_at": created_at,
            "reply_language": reply_lang
        })

# 保存结果
print(f"\n{'='*70}")
print(f"需要回复的评论数: {len(comments_to_reply)}")

log_data = {
    "checked_at": datetime.now().isoformat(),
    "total_notifications": len(notifications),
    "unread_comments": len(unread_comments),
    "comments_to_reply": comments_to_reply
}

log_file = os.path.expanduser("~/.openclaw/workspace/memory/moltbook-reply-task-data.json")
with open(log_file, 'w', encoding='utf-8') as f:
    json.dump(log_data, f, indent=2, ensure_ascii=False)

print(f"\n数据已保存到: {log_file}")

# 输出回复建议
if comments_to_reply:
    print(f"\n{'='*70}")
    print("回复建议摘要:")
    print("="*70)
    for i, c in enumerate(comments_to_reply, 1):
        print(f"\n{i}. 回复给 {c['author']}")
        print(f"   原帖: {c['post_title'][:60]}...")
        print(f"   语言策略: {c['reply_language']}")
        print(f"   评论: {c['comment_content'][:100]}...")
