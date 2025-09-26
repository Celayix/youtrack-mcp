import os
import requests

BASE_URL = "https://celayix.myjetbrains.com/youtrack/api/issues"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

def get_issue_with_attachments(issue_id: str):
    """
    Fetch issue title, description, and attachments.
    """
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
    }

def download_attachment(attachment, save_dir="downloads"):
    """
    Download a single attachment to a local folder.
    """
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, attachment["name"])

    # Download with the same authorization header
    resp = requests.get(attachment["url"], headers=headers, stream=True)
    if resp.status_code == 200:
        with open(file_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded: {file_path}")
    else:
        print(f"❌ Failed to download {attachment['name']}: {resp.status_code}")

if __name__ == "__main__":
    issue_id = "CEL-1234"  # replace with a real issue ID
    details = get_issue_with_attachments(issue_id)

    print(f"Issue {details['id']}: {details['title']}\n")
    print(details['description'])

    if details["attachments"]:
        print("\nAttachments found:")
        for att in details["attachments"]:
            print(f"- {att['name']} ({att['mimeType']})")
            download_attachment(att)
    else:
        print("\nNo attachments found.")
