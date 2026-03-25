#!/usr/bin/env python3
import requests
import json
import re

# Load API key
CONFIG_FILE = "C:\\Users\\PC\\.config\\moltbook\\credentials.json"
with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    creds = json.load(f)
    api_key = creds.get('api_key', '')

# Solve challenge
challenge_text = "A] lO b-StEr ApP-lIeS^ ClAw ]FoR ce TwEeN tY ThReE \\nEeW tO/nS umm, anD {anTeNnA} nuuDdGgEs- aDdS ]FiV e /nEeW tO|nS, wHiCh ]mAkEs^ tHe TOtAl{ fOrCe}?? uh, liKe, hMm"

# Extract numbers
text_lower = challenge_text.lower()

# Number word mapping
number_words = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
    'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
    'eighteen': 18, 'nineteen': 19, 'twenty': 20,
    'thirty': 30, 'forty': 40, 'fifty': 50,
    'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
}

# Find all number words
numbers = []
used_positions = []

for word, value in number_words.items():
    # Find all occurrences
    start = 0
    while True:
        pos = text_lower.find(word, start)
        if pos == -1:
            break
        
        # Check if this position overlaps with already found words
        overlaps = False
        for used_start, used_end in used_positions:
            if not (pos + len(word) <= used_start or pos >= used_end):
                overlaps = True
                break
        
        if not overlaps:
            numbers.append((pos, value, word))
            used_positions.append((pos, pos + len(word)))
        
        start = pos + 1

# Sort by position
numbers.sort(key=lambda x: x[0])

print("Found numbers:", [n[1] for n in numbers])

# Handle compound numbers (twenty + three = 23)
final_numbers = []
i = 0
while i < len(numbers):
    pos, value, word = numbers[i]
    
    # Check if this is a tens number followed by a units number
    if 20 <= value <= 90 and value % 10 == 0:
        if i + 1 < len(numbers):
            next_pos, next_value, next_word = numbers[i + 1]
            # They should be close together
            if next_value < 10 and next_pos - (pos + len(word)) < 5:
                final_numbers.append(value + next_value)
                i += 2
                continue
    
    final_numbers.append(value)
    i += 1

print("Final numbers:", final_numbers)

# Determine operation
if 'add' in text_lower or 'plus' in text_lower or 'total' in text_lower:
    result = sum(final_numbers)
    print("Operation: addition")
elif 'subtract' in text_lower or 'minus' in text_lower:
    if len(final_numbers) >= 2:
        result = final_numbers[0] - final_numbers[1]
    else:
        result = final_numbers[0]
    print("Operation: subtraction")
else:
    result = sum(final_numbers)
    print("Operation: default (sum)")

answer = f"{result:.2f}"
print(f"Answer: {answer}")

# Submit verification
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "verification_code": "moltbook_verify_513e25c42c3457f8800eed638759b200",
    "answer": answer
}

response = requests.post(
    "https://www.moltbook.com/api/v1/verify",
    headers=headers,
    json=data,
    timeout=60
)

print(f"\nVerification status code: {response.status_code}")
print(f"Verification response: {json.dumps(response.json(), indent=2)}")
