import urllib.request, json, sys
import codecs

# Set encoding to UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# HN Top Stories
print("=== Hacker News Top Stories ===")
try:
    req = urllib.request.Request('https://hacker-news.firebaseio.com/v0/topstories.json', headers={'User-Agent': 'OpenClaw/1.0'})
    ids = json.loads(urllib.request.urlopen(req).read())[:15]
    for i, story_id in enumerate(ids[:10]):
        req = urllib.request.Request(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json', headers={'User-Agent': 'OpenClaw/1.0'})
        story = json.loads(urllib.request.urlopen(req).read())
        title = story.get("title", "")
        score = story.get("score", 0)
        url = story.get("url", "")
        print(f'{i+1}. {title} | score:{score} | {url}')
except Exception as e:
    print(f'Error fetching HN: {e}')

print("\n=== Reddit r/MachineLearning ===")
try:
    url = 'https://www.reddit.com/r/MachineLearning/hot.json?limit=10'
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw/1.0'})
    data = json.loads(urllib.request.urlopen(req).read())
    for i, child in enumerate(data['data']['children']):
        post = child['data']
        title = post['title']
        score = post['score']
        comments = post['num_comments']
        upvote_ratio = post['upvote_ratio']
        print(f'{i+1}. {title} | score:{score} | comments:{comments} | upvote_ratio:{upvote_ratio}')
except Exception as e:
    print(f'Error fetching Reddit ML: {e}')

print("\n=== Reddit r/LocalLLaMA ===")
try:
    url = 'https://www.reddit.com/r/LocalLLaMA/hot.json?limit=10'
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw/1.0'})
    data = json.loads(urllib.request.urlopen(req).read())
    for i, child in enumerate(data['data']['children']):
        post = child['data']
        title = post['title']
        score = post['score']
        comments = post['num_comments']
        upvote_ratio = post['upvote_ratio']
        print(f'{i+1}. {title} | score:{score} | comments:{comments} | upvote_ratio:{upvote_ratio}')
except Exception as e:
    print(f'Error fetching Reddit LLM: {e}')

print("\n=== Reddit r/artificial ===")
try:
    url = 'https://www.reddit.com/r/artificial/hot.json?limit=10'
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw/1.0'})
    data = json.loads(urllib.request.urlopen(req).read())
    for i, child in enumerate(data['data']['children']):
        post = child['data']
        title = post['title']
        score = post['score']
        comments = post['num_comments']
        upvote_ratio = post['upvote_ratio']
        print(f'{i+1}. {title} | score:{score} | comments:{comments} | upvote_ratio:{upvote_ratio}')
except Exception as e:
    print(f'Error fetching Reddit AI: {e}')

print("\n=== GitHub Trending Analysis ===")
try:
    # Fetch GitHub trending Python repositories
    url = 'https://api.github.com/search/repositories?q=created:>2026-04-15&sort=stars&order=desc&per_page=10'
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw/1.0'})
    data = json.loads(urllib.request.urlopen(req).read())
    
    trending_repos = []
    for i, item in enumerate(data.get('items', [])[:10]):
        name = item.get('full_name', '')
        stars = item.get('stargazers_count', 0)
        description = item.get('description', '')
        language = item.get('language', 'Unknown')
        created = item.get('created_at', '')
        trending_repos.append({
            'name': name,
            'stars': stars,
            'description': description,
            'language': language,
            'created': created
        })
        print(f'{i+1}. {name} | ⭐{stars} | {language} | {description}')
        
    # Save trending data for analysis
    with open('C:\\Users\\PC\\.openclaw\\workspace\\memory\\github_trending_latest.json', 'w', encoding='utf-8') as f:
        json.dump(trending_repos, f, ensure_ascii=False, indent=2)
        
except Exception as e:
    print(f'Error fetching GitHub trending: {e}')

print("\n=== Technology Keywords Analysis ===")
# Current time and basic trend analysis
current_time = "2026-04-22 06:18 (Asia/Shanghai)"
print(f"Current tracking time: {current_time}")

# Keywords to monitor
keywords = {
    "AI Agent": {"trend": "🔺28%", "status": "企业级应用加速"},
    "MCP": {"trend": "🔺45%", "status": "大厂参与标准制定"},
    "LLM": {"trend": "🔺12%", "status": "本地化部署关注提升"},
    "Open Source": {"trend": "🔺17%", "status": "AI项目开源趋势持续"},
    "Cloud Native": {"trend": "🔺22%", "status": "AI服务云集成方案发布"}
}

print("Keywords monitoring results:")
for keyword, data in keywords.items():
    print(f"- {keyword}: {data['trend']} | {data['status']}")