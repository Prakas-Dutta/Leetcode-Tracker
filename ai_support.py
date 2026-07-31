import json

def build_prompt(pattern_stats, recent, contest_rating=1470):
    return f'''You are a DSA coach. Given a user's solved-problem pattern breakdown, 
    suggest what to practice next. Return ONLY valid JSON, no markdown, no code fences.

    Pattern counts: {pattern_stats}
    Recently solved (last 10): {recent}
    Contest rating: {contest_rating}

    Return JSON in exactly this format:
    {{
    "weak_patterns": ["pattern1", "pattern2"],
    "reasoning": "1-2 sentences",
    "suggested_focus": "pattern name",
    "suggested_problems": [{{ "name": "Problem name 1", "url": "https://leetcode.com/problems/problem-1/" }}, {{ "name": "Problem name 2", "url": "https://leetcode.com/problems/problem-2/" }}, {{ "name": "Problem name 3", "url": "https://leetcode.com/problems/problem-3/" }}]
    }}'''




def extract_json(raw_text: str) -> dict:
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    return json.loads(text)



