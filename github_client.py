from github import Github
import os

def get_github_client():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Set GITHUB_TOKEN environment variable first")
    return Github(token)