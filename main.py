from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from domain import game_router, user_router
from database import Base, engine, SessionLocal
from models import Item 

# ─── 이미지 서버 URL을 한 곳에 선언 ───────────────────────
BASE_URL = "https://cdn.example.com/images/"
# ──────────────────────────────────────────────────────────

app = FastAPI()

# DB 테이블이 없으면 생성
Base.metadata.create_all(bind=engine)

# 기존 라우터 등록
app.include_router(game_router.router)
app.include_router(user_router.router)

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 예시: 아이템 조회 엔드포인트에서 image_url 조합
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # DB에 저장된 키(key)와 BASE_URL을 합쳐 최종 URL 생성
    full_url = f"{BASE_URL}{item.image_key}"
    return {
        "id": item.id,
        "name": item.name,
        "image_url": full_url
    }



