import requests
import base64
import json
import sys
import os

def deploy(token, repo, path, html_content):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get SHA
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sha = r.json()['sha']
    else:
        sha = None # New file

    # Encode
    encoded = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')

    payload = {
        "message": "Update broken-line-search.html via Skill",
        "content": encoded
    }
    if sha:
        payload["sha"] = sha

    # Push
    r = requests.put(url, headers=headers, data=json.dumps(payload))
    if r.status_code in [200, 201]:
        print(f"Successfully deployed to {repo}/{path}")
    else:
        print(f"Failed to deploy: {r.status_code}")
        print(r.text)
        sys.exit(1)

if __name__ == "__main__":
    # Example usage: python deploy.py <token> <repo> <path> <local_file_path>
    if len(sys.argv) < 5:
        print("Usage: python deploy.py <token> <repo> <path> <local_file_path>")
        sys.exit(1)
    
    token = sys.argv[1]
    repo = sys.argv[2]
    path = sys.argv[3]
    local_file = sys.argv[4]
    
    with open(local_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    deploy(token, repo, path, content)
