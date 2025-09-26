import requests

BASE_URL = "https://celayix.myjetbrains.com/youtrack/api/issues"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

def get_issue_with_attachments(issue_id: str):
    """
    Fetch issue title, description, and attachments (e.g. images).
    """
    url = f"{BASE_URL}/{issue_id}"
    params = {
        "fields": "idReadable,summary,description,attachments(name,url,mimeType)"
    }
    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code != 200:
        raise Exception(f"Error {resp.status_code}: {resp.text}")

    issue = resp.json()
    attachments = [
        {
            "name": a["name"],
            "url": a["url"],
            "mimeType": a["mimeType"]
        }
        for a in issue.get("attachments", [])
    ]
    return {
        "id": issue.get("idReadable"),
        "title": issue.get("summary"),
        "description": issue.get("description"),
        "attachments": attachments
    }

# Example usage
if __name__ == "__main__":
    issue_id = "SXM-470"  # replace with a real issue ID given by user
    details = get_issue_with_attachments(issue_id)
    print(f"Issue {details['id']}: {details['title']}\n")
    print(details['description'])
    if details["attachments"]:
        print("\nAttachments:")
        for att in details["attachments"]:
            print(f"- {att['name']} ({att['mimeType']}): {BASE_URL}{att['url']}")
