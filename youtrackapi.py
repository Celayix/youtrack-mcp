import requests

# Replace with your YouTrack Cloud domain (no trailing slash)
BASE_URL = "https://celayix.myjetbrains.com/youtrack/api/issues"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

def get_issue_details(issue_id: str):
    """
    Retrieve issue title and description for a given issue ID.
    """
    url = f"{BASE_URL}/{issue_id}"
    params = {
        "fields": "idReadable,summary,description"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        issue = response.json()
        return {
            "id": issue.get("idReadable"),
            "title": issue.get("summary"),
            "description": issue.get("description")
        }
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Example usage
if __name__ == "__main__":
    issue_id = "CEL-1234"  # replace with issue ID given by user
    details = get_issue_details(issue_id)
    print(f"Issue {details['id']}: {details['title']}\n\n{details['description']}")
