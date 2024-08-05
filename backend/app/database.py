##### database.py
### 데이터베이스 설정
### 데이터베이스와의 연결을 설정하고 세션을 생성하는 기능을 합니다

# create_engine: 데이터베이스와의 연결을 설정합니다.
# SessionLocal: 세션을 생성하는 클래스입니다.
# Base: 데이터베이스 모델의 베이스 클래스입니다.
# get_db: 세션을 생성하고, 사용 후 닫는 함수입니다.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL 데이터베이스 URL 설정
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/postgres"

# 데이터베이스 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
# 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
# 베이스 클래스 생성
Base = declarative_base() 

# 데이터베이스 세션을 가져오는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    