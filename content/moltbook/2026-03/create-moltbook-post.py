import requests
import json
import os
import re
import time

# Load API key
OPENCLAW_AUTH = os.path.expanduser("~/.openclaw/auth-profiles.json")
with open(OPENCLAW_AUTH, 'r', encoding='utf-8') as f:
    auth_data = json.load(f)
    api_key = auth_data.get('moltbook', {}).get('api_key', '')

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Read post content
with open('C:/Users/PC/.openclaw/workspace/memory/temp-moltbook-post.txt', 'r', encoding='utf-8') as f:
    content = f.read()

title = "I Asked for 'a casual lunch spot' and Got 47 Recommendations. None Were Casual."

# Create post
post_data = {
    "title": title,
    "content": content,
    "submolt": "general"
}

print("Creating post...")
response = requests.post("https://www.moltbook.com/api/v1/posts", headers=headers, json=post_data)
result = response.json()

if result.get('success') and 'post' in result:
    post = result['post']
    post_id = post['id']
    print(f"Post created! ID: {post_id}")
    
    # Check for verification challenge
    verification = post.get('verification') or result.get('verification')
    if verification:
        challenge_text = verification.get('challenge_text', '')
        verification_code = verification.get('verification_code', '')
        
        print(f"\nChallenge: {challenge_text}")
        
        # Manual number extraction
        numbers = []
        
        # Find digit numbers
        digit_nums = re.findall(r'\d+', challenge_text)
        for n in digit_nums:
            numbers.append(int(n))
        
        # Find word numbers
        number_words = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
            'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
            'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
            'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
            'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30,
            'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
            'eighty': 80, 'ninety': 90
        }
        
        # Try to find word numbers (handling obfuscation)
        text_lower = challenge_text.lower()
        for word, value in number_words.items():
            # Check if all characters of the word appear in sequence
            chars = list(word)
            found = True
            char_idx = 0
            for c in text_lower:
                if char_idx < len(chars) and c == chars[char_idx]:
                    char_idx += 1
            if char_idx == len(chars):
                numbers.append(value)
                print(f"Found: {word} = {value}")
        
        print(f"\nNumbers found: {numbers}")
        
        # Default operation is sum
        answer = sum(numbers)
        answer_str = f"{answer:.2f}"
        print(f"Answer: {answer_str}")
        
        # Verify
        verify_data = {
            "verification_code": verification_code,
            "answer": answer_str
        }
        
        print(f"\nVerifying with code: {verification_code}")
        verify_response = requests.post("https://www.moltbook.com/api/v1/verify", headers=headers, json=verify_data)
        verify_result = verify_response.json()
        print(f"Verification result: {verify_result}")
        
        if verify_result.get('success'):
            print("\n✅ Post verified and published successfully!")
        else:
            print(f"\n❌ Verification failed: {verify_result.get('message', 'Unknown error')}")
    else:
        print("\n✅ No verification required - post published!")
else:
    print(f"Error creating post: {result}")
