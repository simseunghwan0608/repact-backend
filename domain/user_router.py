from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from domain import user_schema
from models import User
from security import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_create.username).first()
    if user:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")

    new_user = User(
        name=user_create.name,
        username=user_create.username,
        hashed_password=hash_password(user_create.password),
        phone=user_create.phone,
        email=user_create.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "회원가입이 완료되었습니다."}

@router.post("/login")
def login(user_login: user_schema.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}
