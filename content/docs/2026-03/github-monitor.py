import subprocess
import json
from datetime import datetime
import os
import sys

# Force UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

gh_path = r"C:\Program Files\GitHub CLI\gh.exe"

# Get latest issues using gh api
result = subprocess.run(
    [gh_path, "api", "repos/ava-agent/ai-ideas/issues?state=open&per_page=15&sort=created&direction=desc"],
    capture_output=True,
    encoding='utf-8'
)

if result.returncode != 0:
    print(f"Error: {result.stderr}")
    exit(1)

issues_data = json.loads(result.stdout)

# Get latest PRs
result = subprocess.run(
    [gh_path, "api", "repos/ava-agent/ai-ideas/pulls?state=all&per_page=15&sort=created&direction=desc"],
    capture_output=True,
    encoding='utf-8'
)

if result.returncode != 0:
    print(f"Error: {result.stderr}")
    exit(1)

prs_data = json.loads(result.stdout)

# Save to file for later processing
output = {
    "timestamp": datetime.now().isoformat(),
    "issues": issues_data,
    "prs": prs_data
}

with open("memory/github-latest-data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Data saved to memory/github-latest-data.json")
print(f"Found {len(issues_data)} issues and {len(prs_data)} PRs")
