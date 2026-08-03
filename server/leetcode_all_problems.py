

import sys
import json
import csv
import requests

ALL_PROBLEMS_URL = "https://leetcode.com/api/problems/all/"

HEADERS = {
    "Referer": "https://leetcode.com",
    "User-Agent": "Mozilla/5.0",
}

DIFFICULTY_MAP = {1: "Easy", 2: "Medium", 3: "Hard"}


def fetch_all_problems() -> list[dict]:
    resp = requests.get(ALL_PROBLEMS_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    problems = []
    for item in data.get("stat_status_pairs", []):
        stat = item["stat"]
        problems.append([
            stat["frontend_question_id"],
            stat["question__title"],
            DIFFICULTY_MAP.get(item["difficulty"]["level"], "Unknown")
        ])

    problems.sort(key=lambda p: p[0])
    return problems




