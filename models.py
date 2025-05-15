from sqlalchemy import Column, Integer, String, JSON
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    total_score = Column(Integer, default=0)

class Trash(Base):
    __tablename__ = "trash"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)    
    correctBin = Column(String, nullable=False)
    specificBin = Column(String, nullable=False)
    messageInitial = Column(String, nullable=False)   
    messageCorrect = Column(String, nullable=False)    
    messageInCorrect = Column(String, nullable=False)         
    difficulty = Column(Integer, nullable=False, default=1)
    score = Column(Integer, nullable=False, default=10)
    image_key = Column(String, nullable=False) # 각 아이템이 사용할 이미지 파일의 경로(예: "avatars/123.png")를 DB에 채워 넣어야 함
    type_2_seq = Column(JSON)
    type_2_seq_ans = Column(JSON)


class comment(Base):
    __tablename__ = "comment"

    comments = Column(JSON)
