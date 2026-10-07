from fastapi import FastAPI
import uvicorn

app = FastAPI()

FAKE_ISSUES = {
    1: {"number": 1, "title": "Login button broken", "body": "Clicking login does nothing."},
    2: {"number": 2, "title": "Add dark mode", "body": "Please add a dark theme option."},
}


@app.get("/repos/{owner}/{repo}/issues/{issue_number}")
def get_issue(owner: str, repo: str, issue_number: int):
    return FAKE_ISSUES.get(issue_number, {"number": issue_number, "title": "Not found", "body": ""})


@app.get("/repos/{owner}/{repo}/issues")
def list_issues(owner: str, repo: str):
    return list(FAKE_ISSUES.values())


@app.post("/repos/{owner}/{repo}/issues/{issue_number}/comments")
def create_comment(owner: str, repo: str, issue_number: int, payload: dict):
    return {
        "html_url": f"http://localhost:8080/{owner}/{repo}/issues/{issue_number}#comment",
        "body": payload.get("body"),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
