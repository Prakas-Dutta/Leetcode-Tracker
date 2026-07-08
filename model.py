from pydantic import BaseModel

class Problem(BaseModel):
        leetcode_id: int
        title: str
        difficulty: str
        approach: str