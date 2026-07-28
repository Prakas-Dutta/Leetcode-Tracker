import httpx
from datetime import datetime

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

RECENT_SUBMISSIONS_QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
  }
}
"""

async def get_recent_leetcode_solutions(leetcode_username: str, limit: int = 20):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            LEETCODE_GRAPHQL_URL,
            json={
                "query": RECENT_SUBMISSIONS_QUERY,
                "variables": {"username": leetcode_username, "limit": limit}
            },
            headers={
                "Content-Type": "application/json",
                "Referer": f"https://leetcode.com/{leetcode_username}/"
            }
        )
        resp.raise_for_status()
        data = resp.json()

    submissions = data["data"]["recentAcSubmissionList"]

    for sub in submissions:
        sub["date"] = datetime.utcfromtimestamp(int(sub["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")

    return submissions