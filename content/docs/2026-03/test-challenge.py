import sys
sys.path.insert(0, 'C:/Users/PC/.openclaw/workspace/skills/moltbook-interact/scripts')

from moltbook import solve_challenge

# Test challenges from previous attempts
challenges = [
    "LoB]sT-Er LoOoobsssTEr^ ClAw~ FoRcE Is- TwEnTy ]FiVe NeW/ToN",
    "ThIs] Lo.oBbSsTtEeRr\\ ClAw- ExEeRrTtS^ FoRrTtY{ NeOoTtOnNs",
    "A] Lo.bStEr S^wImS[ aT/ TwEnTy ThReE CeMmEeNtErS PeR SeCoNd, \\\\ um LoOooBstEr AntEnNaS ToUcH, ClAw FoRcE Is^ FiFtEeN NeWtOnS, ~ MuLtIpLy ThEm?>"
]

for i, challenge in enumerate(challenges, 1):
    print(f"\nChallenge {i}:")
    print(f"Text: {challenge}")
    answer = solve_challenge(challenge)
    print(f"Answer: {answer}")
