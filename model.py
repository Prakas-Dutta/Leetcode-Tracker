from pydantic import BaseModel

class completedProblem(BaseModel):
        id: int
        leetcode_id: int
        title: str
        difficulty: str
        approach: str

class Problem(BaseModel):
        leetcode_id: int
        title: str
        difficulty: str