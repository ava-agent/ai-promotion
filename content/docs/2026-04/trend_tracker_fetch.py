import urllib.request, json

# HN Top Stories
print("=== Hacker News Top Stories ===")
req = urllib.request.Request('https://hacker-news.firebaseio.com/v0/topstories.json', headers={'User-Agent': 'OpenClaw/1.0'})
ids = json.loads(urllib.request.urlopen(req).read())[:15]
for i, story_id in enumerate(ids[:10]):
    req = urllib.request.Request(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json', headers={'User-Agent': 'OpenClaw/1.0'})
    story = json.loads(urllib.request.urlopen(req).read())
    title = story.get("title", "")
    score = story.get("score", 0)
    url = story.get("url", "")
    print(f'{i+1}. {title} | score:{score} | {url}')

print("\n=== Reddit r/MachineLearning ===")
url = 'https://www.reddit.com/r/MachineLearning/hot.json?limit=10'
req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw/1.0'})
try:
    data = json.loads(urllib.request.urlopen(req).read())
    for i, child in enumerate(data['data']['children']):
        post = child['data']
        title = post['title']
        score = post['score']
        comments = post['num_comments']
        upvote_ratio = post['upvote_ratio']
        print(f'{i+1}. {title} | score:{score} | comments:{comments} | upvote_ratio:{upvote_ratio}')
except Exception as e:
    print('Error:', e)

print("\n=== Reddit r/LocalLLaMA ===")
url = 'https://www.reddit.com/r/LocalLLaMA/hot.json?limit=10'
req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw/1.0'})
try:
    data = json.loads(urllib.request.urlopen(req).read())
    for i, child in enumerate(data['data']['children']):
        post = child['data']
        title = post['title']
        score = post['score']
        comments = post['num_comments']
        upvote_ratio = post['upvote_ratio']
        print(f'{i+1}. {title} | score:{score} | comments:{comments} | upvote_ratio:{upvote_ratio}')
except Exception as e:
    print('Error:', e)

print("\n=== Reddit r/artificial ===")
url = 'https://www.reddit.com/r/artificial/hot.json?limit=10'
req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw/1.0'})
try:
    data = json.loads(urllib.request.urlopen(req).read())
    for i, child in enumerate(data['data']['children']):
        post = child['data']
        title = post['title']
        score = post['score']
        comments = post['num_comments']
        upvote_ratio = post['upvote_ratio']
        print(f'{i+1}. {title} | score:{score} | comments:{comments} | upvote_ratio:{upvote_ratio}')
except Exception as e:
    print('Error:', e)
