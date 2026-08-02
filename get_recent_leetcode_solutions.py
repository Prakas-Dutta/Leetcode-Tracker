import httpx
from datetime import datetime

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

COMBINED_QUERY = """
query getUserProfileData($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
  }
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    totalParticipants
    topPercentage
    badge {
      name
    }
  }
}
"""


def _headers(username: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/{username}/"
    }


async def get_leetcode_profile_data(leetcode_username: str, limit: int = 20):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            LEETCODE_GRAPHQL_URL,
            json={
                "query": COMBINED_QUERY,
                "variables": {"username": leetcode_username, "limit": limit}
            },
            headers=_headers(leetcode_username)
        )
        resp.raise_for_status()
        data = resp.json()

    if data.get("errors"):
        raise ValueError(f"GraphQL error: {data['errors']}")

    result = data["data"]

    # Process recent submissions
    submissions = result["recentAcSubmissionList"]
    for sub in submissions:
        sub["date"] = datetime.utcfromtimestamp(int(sub["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")

    # Process contest ranking
    ranking = result["userContestRanking"]
    if ranking is None:
        contest_data = {"attended": False, "message": "User has not participated in any rated contest."}
    else:
        contest_data = {
            "attended": True,
            "rating": round(ranking["rating"], 2),
            "global_ranking": ranking["globalRanking"],
            "total_participants": ranking["totalParticipants"],
            "top_percentage": ranking["topPercentage"],
            "attended_contests_count": ranking["attendedContestsCount"],
            "badge": ranking["badge"]["name"] if ranking["badge"] else None
        }

    return {
        "recent_submissions": submissions,
        "contest_ranking": contest_data
    }