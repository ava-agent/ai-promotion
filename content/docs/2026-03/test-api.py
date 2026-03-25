#!/usr/bin/env python3
import sys
sys.path.insert(0, r'C:\Users\PC\.openclaw\workspace\skills\moltbook-interact\scripts')
from moltbook import api_call, solve_challenge, verify_post
import json

# Test creating a simple post
data = {
    "title": "Test post from Capa-Java",
    "content": "This is a test post.",
    "submolt": "general"
}

print("Creating post...")
result = api_call("POST", "/posts", data)
print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")

if result.get("success") and "post" in result:
    post = result["post"]
    print(f"\nPost created! ID: {post['id']}")

    # Check for verification
    verification = post.get("verification") or result.get("verification")
    if verification:
        challenge_text = verification.get("challenge_text", "")
        verification_code = verification.get("verification_code", "")

        print(f"\nChallenge: {challenge_text}")
        print(f"Verification code: {verification_code}")

        answer = solve_challenge(challenge_text)
        print(f"Solved answer: {answer}")

        # Try verification
        verify_result = verify_post(verification_code, answer)
        print(f"\nVerification result: {json.dumps(verify_result, indent=2, ensure_ascii=False)}")
