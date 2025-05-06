from pydantic import BaseModel

class GameStartResponse(BaseModel):
    trash_id: int
    name: str
    difficulty: int

class GameSubmitRequest(BaseModel):
    trash_id: int
    selected_category: str

class GameSubmitResponse(BaseModel):
    correct: bool
    time_over: bool
    earned_score: int
    total_score: int
