"""
LeetCode Problem Details Fetcher (by number)
---------------------------------------------
Fetches full details for a LeetCode problem using just its problem
number (the frontend ID shown on leetcode.com, e.g. 1 for "Two Sum").

Usage:
    python leetcode_problem.py <problem-number>

Example:
    python leetcode_problem.py 1
    python leetcode_problem.py 3
"""

import sys
import json
import re
import requests

GRAPHQL_URL = "https://leetcode.com/graphql"
ALL_PROBLEMS_URL = "https://leetcode.com/api/problems/all/"

HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "User-Agent": "Mozilla/5.0",
}

QUESTION_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    title
    titleSlug
    difficulty
    likes
    dislikes
    isPaidOnly
    content
    exampleTestcases
    hints
    topicTags {
      name
      slug
    }
    stats
    similarQuestions
  }
}
"""


def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    text = re.sub(r"<[^>]+>", "", raw_html)
    text = text.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
    return text.strip()


def slug_from_number(problem_number: int) -> str:
    """Look up a problem's slug from its frontend number using LeetCode's
    legacy 'all problems' endpoint (contains id -> slug mapping)."""
    resp = requests.get(ALL_PROBLEMS_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    for item in data.get("stat_status_pairs", []):
        stat = item["stat"]
        if stat["frontend_question_id"] == problem_number:
            return stat["question__title_slug"]

    raise ValueError(f"No problem found with number {problem_number}")


def get_problem_by_number(problem_number: int) -> dict:
    slug = slug_from_number(problem_number)

    resp = requests.post(
        GRAPHQL_URL,
        headers=HEADERS,
        json={"query": QUESTION_QUERY, "variables": {"titleSlug": slug}},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])

    q = data["data"]["question"]
    if q is None:
        raise ValueError(f"Problem slug '{slug}' not found via GraphQL")

    stats = json.loads(q["stats"]) if q.get("stats") else {}
    similar = json.loads(q["similarQuestions"]) if q.get("similarQuestions") else []

    return {
        "id": q["questionFrontendId"],
        "title": q["title"],
        "difficulty": q["difficulty"],
    }


if __name__ == "__main__":

    number = 1
    try:
        problem = get_problem_by_number(number)
        print(json.dumps(problem, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
