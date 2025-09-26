import os
import sys
import requests

BASE_URL = "https://celayix.myjetbrains.com/youtrack/api/issues"

def get_issue_with_attachments(issue_id: str, token: str):
    """
    Fetch issue title, description, and attachments.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = f"{BASE_URL}/{issue_id}"
    params = {
        "fields": "idReadable,summary,description,attachments(name,url,mimeType)"
    }
    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code != 200:
        raise Exception(f"Error {resp.status_code}: {resp.text}")

    issue = resp.json()
    attachments = issue.get("attachments", [])
    return {
        "id": issue.get("idReadable"),
        "title": issue.get("summary"),
        "description": issue.get("description"),
        "attachments": attachments
    }, headers


def download_attachment(attachment, headers, save_dir="downloads"):
    """
    Download a single attachment to a local folder.
    """
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, attachment["name"])

    resp = requests.get(attachment["url"], headers=headers, stream=True)
    if resp.status_code == 200:
        with open(file_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded: {file_path}")
    else:
        print(f"❌ Failed to download {attachment['name']}: {resp.status_code}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <ISSUE_ID> <TOKEN>")
        sys.exit(1)

    issue_id = sys.argv[1]
    token = sys.argv[2]

    details, headers = get_issue_with_attachments(issue_id, token)

    print(f"Issue {details['id']}: {details['title']}\n")
    print(details['description'])

    if details["attachments"]:
        print("\nAttachments found:")
        for att in details["attachments"]:
            print(f"- {att['name']} ({att['mimeType']})")
            download_attachment(att, headers)
    else:
        print("\nNo attachments found.")
