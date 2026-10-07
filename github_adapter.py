import requests
from config import GITHUB_API_BASE, GITHUB_TOKEN


class GitHubClient:
    def __init__(self, base_url: str = GITHUB_API_BASE, token: str = GITHUB_TOKEN):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }

    def get_issue(self, owner: str, repo: str, issue_number: int) -> dict:
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def list_issues(self, owner: str, repo: str) -> list:
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def create_comment(self, owner: str, repo: str, issue_number: int, body: str) -> dict:
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        resp = requests.post(url, headers=self.headers, json={"body": body}, timeout=10)
        resp.raise_for_status()
        return resp.json()
