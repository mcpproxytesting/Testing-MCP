import sys
from mcp.server import MCPServer
from github_adapter import GitHubClient

mcp = MCPServer("target-github-server")
gh = GitHubClient()


@mcp.tool()
def get_issue(owner: str, repo: str, issue_number: int) -> str:
    """Fetch a single GitHub issue by number."""
    issue = gh.get_issue(owner, repo, issue_number)
    return f"#{issue['number']} {issue['title']}: {issue.get('body', '')}"


@mcp.tool()
def list_issues(owner: str, repo: str) -> str:
    """List open issues for a repository."""
    issues = gh.list_issues(owner, repo)
    return "\n".join(f"#{i['number']} {i['title']}" for i in issues) or "No issues found."


@mcp.tool()
def comment_on_issue(owner: str, repo: str, issue_number: int, body: str) -> str:
    """Post a comment on a GitHub issue."""
    result = gh.create_comment(owner, repo, issue_number, body)
    return f"Comment posted: {result.get('html_url', 'ok')}"


if __name__ == "__main__":
    print("MCP server starting (stdio transport)...", file=sys.stderr)
    mcp.run(transport="stdio")
