import requests

# Replace with your YouTrack Cloud domain (no trailing slash)
BASE_URL = "https://celayix.myjetbrains.com/youtrack/api/issues"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

# YouTrack query language: filter issues by tag 'codex'
params = {
    "query": "tag: codex",
    "fields": "idReadable,summary,tags(name),created,reporter(fullName)",
    "$top": 100  # fetch up to 100 issues in one request
}

response = requests.get(BASE_URL, headers=headers, params=params)

if response.status_code == 200:
    issues = response.json()
    if not issues:
        print("No issues found with tag 'codex'.")
    else:
        for issue in issues:
            tags = [t["name"] for t in issue.get("tags", [])]
            print(f"{issue['idReadable']}: {issue['summary']} | Tags: {tags}")
else:
    print("Error:", response.status_code, response.text)
