from github import Github
from github.Auth import AppAuth
import os

def get_github_client():
    app_id = int(os.getenv("GITHUB_APP_ID"))
    installation_id = int(os.getenv("GITHUB_INSTALLATION_ID"))
    private_key_path = os.getenv("GITHUB_PRIVATE_KEY_PATH")

    with open(private_key_path, "r") as f:
        private_key = f.read()

    # 1. Create App authentication
    app_auth = AppAuth(app_id, private_key)

    # 2. Create installation token
    installation_auth = app_auth.get_installation_auth(installation_id)

    # 3. Create GitHub client using installation token
    return Github(auth=installation_auth)
