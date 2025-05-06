import random
from sqlalchemy.orm import Session
from models import Trash, User
from datetime import datetime, timedelta

def get_random_trash(db: Session):
    trash_list = db.query(Trash).all()
    return random.choice(trash_list)

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def update_user_score(db: Session, user: User, earned_score: int):
    user.total_score += earned_score
    db.commit()

def is_time_over(start_time: datetime, limit_seconds: int = 30):
    now = datetime.utcnow()
    return (now - start_time).total_seconds() > limit_seconds
