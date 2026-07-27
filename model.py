from pydantic import BaseModel

class CompletedProblem(BaseModel):
        leetcode_id:int
        approach: str

class Problem(BaseModel):
        leetcode_id: int
        title: str
        difficulty: str

class UpdatedInfo(BaseModel):
        leetcode_id:int
        approach:str
        updated_approach:str