import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('moltbook-notifications.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter unread comment notifications
unread_comments = []
for notif in data.get('notifications', []):
    if notif.get('isRead') == False and notif.get('type') == 'post_comment':
        comment = notif.get('comment', {})
        post = notif.get('post', {})
        unread_comments.append({
            'notification_id': notif.get('id'),
            'comment_id': comment.get('id'),
            'comment_content': comment.get('content', ''),
            'is_crypto': comment.get('isCrypto', False),
            'is_spam': comment.get('isSpam', False),
            'post_id': post.get('id'),
            'post_title': post.get('title', ''),
            'created_at': notif.get('createdAt')
        })

print(f'Found {len(unread_comments)} unread comment notifications:\n')
for i, c in enumerate(unread_comments, 1):
    print(f"{i}. Post: {c['post_title'][:60]}")
    print(f"   Comment: {c['comment_content'][:150]}")
    print(f"   Crypto: {c['is_crypto']}, Spam: {c['is_spam']}")
    print(f"   Comment ID: {c['comment_id']}")
    print(f"   Post ID: {c['post_id']}")
    print()
