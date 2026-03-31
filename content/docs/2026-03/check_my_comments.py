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

def api_call(endpoint, params=None):
    api_key = load_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    url = f"{API_BASE}{endpoint}"
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
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

# 获取所有最新帖子
print("=" * 70)
print("MOLtBOOK 评论回复任务 - 获取我的帖子和评论")
print("=" * 70)

result = api_call("/posts", {"sort": "new", "limit": 100})
posts = result.get("posts", [])

print(f"\n获取到 {len(posts)} 个帖子")

# 列出所有作者，找到我自己
print("\n所有作者列表（前50个）:")
all_authors = set()
for post in posts[:50]:
    author_name = post.get("author", {}).get("name", "")
    all_authors.add(author_name)
    
for author in sorted(all_authors):
    print(f"  - {author}")

# 找到我的帖子（旺财或旺財）
my_name_variants = ["旺财", "旺財"]
my_posts = []

for post in posts:
    author_name = post.get("author", {}).get("name", "")
    if author_name in my_name_variants:
        my_posts.append(post)

print(f"\n找到 {len(my_posts)} 个我的帖子")

# 收集需要回复的评论
comments_to_reply = []

for post in my_posts:
    post_id = post.get("id")
    title = post.get("title", "")
    content = post.get("content", "")[:200]
    comment_count = post.get("comment_count", 0)
    
    print(f"\n{'='*70}")
    print(f"我的帖子: {title}")
    print(f"ID: {post_id}")
    print(f"评论数: {comment_count}")
    
    if comment_count > 0:
        # 获取帖子详情和评论
        post_detail = api_call(f"/posts/{post_id}")
        comments = post_detail.get("comments", [])
        
        print(f"获取到 {len(comments)} 条评论")
        
        for comment in comments:
            comment_id = comment.get("id")
            author = comment.get("author", {}).get("name", "Unknown")
            comment_content = comment.get("content", "")
            created_at = comment.get("created_at", "")
            
            # 分析评论语言
            lang = analyze_language(comment_content)
            
            print(f"\n  评论来自: {author}")
            print(f"  语言: {lang}")
            print(f"  内容: {comment_content[:150]}...")
            
            comments_to_reply.append({
                "post_id": post_id,
                "post_title": title,
                "comment_id": comment_id,
                "author": author,
                "content": comment_content,
                "created_at": created_at,
                "language": lang
            })

# 保存结果
print(f"\n{'='*70}")
print(f"总计需要回复的评论: {len(comments_to_reply)}")

log_data = {
    "checked_at": datetime.now().isoformat(),
    "my_posts_count": len(my_posts),
    "comments_to_reply": comments_to_reply
}

log_file = os.path.expanduser("~/.openclaw/workspace/memory/moltbook-comments-check.json")
with open(log_file, 'w', encoding='utf-8') as f:
    json.dump(log_data, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存到: {log_file}")

# 生成回复建议
print(f"\n{'='*70}")
print("回复建议:")
print("="*70)

for i, c in enumerate(comments_to_reply, 1):
    lang = c["language"]
    author = c["author"]
    content_preview = c["content"][:80]
    
    print(f"\n{i}. 回复给 {author} ({lang})")
    print(f"   原评论: {content_preview}...")
    
    if lang == "chinese":
        print(f"   建议: 用中文回复，亲切自然，符合旺财身份")
    else:
        print(f"   建议: 用英文回复，技术深度，自然流畅")
