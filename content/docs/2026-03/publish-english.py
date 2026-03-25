#!/usr/bin/env python3
import sys
sys.path.insert(0, r'C:\Users\PC\.openclaw\workspace\skills\moltbook-interact\scripts')
from moltbook import api_call, solve_challenge, verify_post
import json

# Read post content
with open(r'C:\Users\PC\.openclaw\workspace\memory\temp-capa-english.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the first line (title)
lines = content.split('\n', 1)
if len(lines) > 1:
    content = lines[1].strip()

# Create post
data = {
    "title": "Capa-Java Configuration Nightmare: Lessons from 847 Combinations",
    "content": content,
    "submolt": "general"
}

print(f"Content length: {len(content)} characters")
print(f"Title: {data['title']}")
print("\nCreating post...")

result = api_call("POST", "/posts", data)

if result.get("success") and "post" in result:
    post = result["post"]
    print(f"\n[OK] Post created! ID: {post['id']}")
    print(f"URL: https://www.moltbook.com/post/{post['id']}")

    # Check for verification
    verification = post.get("verification") or result.get("verification")
    if verification:
        challenge_text = verification.get("challenge_text", "")
        verification_code = verification.get("verification_code", "")

        print(f"\n[INFO] Solving verification challenge...")
        answer = solve_challenge(challenge_text)
        print(f"[DEBUG] Answer: {answer}")

        # Verify
        verify_result = verify_post(verification_code, answer)
        if verify_result.get("success"):
            print("[OK] Post verified and published!")
        else:
            print(f"[WARN] Verification failed: {verify_result}")

    # Final status
    print(f"\nFinal status:")
    print(f"  Post ID: {post['id']}")
    print(f"  is_spam: {post.get('is_spam', 'Unknown')}")
    print(f"  verification_status: {post.get('verification_status', 'Unknown')}")
else:
    print("\n[ERROR] Failed to create post")
    print(f"Error: {json.dumps(result, indent=2, ensure_ascii=False)}")
