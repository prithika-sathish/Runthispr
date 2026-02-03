from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from github_client import get_github_client

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    event_type = request.headers.get("X-GitHub-Event")

    if event_type != "pull_request":
        return {"status": "ignored"}

    payload = await request.json()
    action = payload.get("action")

    if action not in {"opened", "synchronize", "reopened"}:
        return {"status": "ignored"}

    repo_full_name = payload["repository"]["full_name"]
    pr_number = payload["pull_request"]["number"]

    print("Accepted PR event")
    print("Action:", action)
    print("Repo:", repo_full_name)
    print("PR number:", pr_number)

    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)

    print("Title:", pr.title)
    print("Author:", pr.user.login)
    print("Base branch:", pr.base.ref)
    print("Head branch:", pr.head.ref)
    print("Commits:", pr.commits)
    print("Files changed:", pr.changed_files)
    print("Additions:", pr.additions)
    print("Deletions:", pr.deletions)

    return {"status": "processed"}
