from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from domain import game_schema
from models import Trash, User
from datetime import datetime
from domain import game_service

router = APIRouter()

current_trash = None
current_start_time = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/game/start", response_model=game_schema.GameStartResponse)
def game_start(db: Session = Depends(get_db)):
    global current_trash
    global current_start_time
    trash = game_service.get_random_trash(db)
    current_start_time = datetime.utcnow()
    current_trash = trash
    return game_schema.GameStartResponse(
        trash_id=trash.id,
        name=trash.name,
        difficulty=trash.difficulty
    )

@router.post("/game/submit", response_model=game_schema.GameSubmitResponse)
def game_submit(
    request: game_schema.GameSubmitRequest,
    db: Session = Depends(get_db),
    username: str = None  # (나중에 JWT로 받을 예정)
):
    global current_trash
    global current_start_time

    if current_trash is None or current_start_time is None:
        raise HTTPException(status_code=400, detail="게임을 시작하지 않았습니다.")

    if request.trash_id != current_trash.id:
        raise HTTPException(status_code=400, detail="잘못된 쓰레기입니다.")

    user = None
    if username:
        user = game_service.get_user_by_username(db, username)

    correct = current_trash.category == request.selected_category
    time_over = game_service.is_time_over(current_start_time)

    earned_score = 0
    if correct and not time_over:
        earned_score = current_trash.score
        if user:
            game_service.update_user_score(db, user, earned_score)

    return game_schema.GameSubmitResponse(
        correct=correct,
        time_over=time_over,
        earned_score=earned_score,
        total_score=user.total_score if user else 0
    )
