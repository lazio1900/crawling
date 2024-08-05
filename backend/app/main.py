##### main.py
### FastAPI 설정
### 이 파일은 FastAPI 애플리케이션을 설정하고, API 엔드포인트를 정의합니다.

# Base.metadata.create_all(bind=engine): 데이터베이스 테이블을 생성합니다.
# app = FastAPI(): FastAPI 애플리케이션을 생성합니다.
# API 엔드포인트: 데이터베이스에 데이터를 추가하는 API를 정의합니다.

from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app import models, crud
from app.database import engine, Base, get_db
from app.crawler import SIMPJT_crawling

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# apartment_complex_basic Table 생성
@app.post("/apartment-complex/")
def create_apartment_complex(complex_data: dict, db: Session = Depends(get_db)):
    return crud.create_apartment_complex_basic(db=db, complex_data=complex_data)

# apartment_complex_details Table 생성
@app.post("/apartment-complex/details/")
def create_apartment_complex_details(details_data: dict, db: Session = Depends(get_db)):
    return crud.create_apartment_complex_details(db=db, details_data=details_data)

# create_crawling_data Table 생성
@app.post("/crawling-data/")
def create_crawling_data(crawling_data: dict, db: Session = Depends(get_db)):
    return crud.create_crawling_data(db=db, crawling_data=crawling_data)

# crawl 실행
@app.post("/crawl/")
def trigger_crawling(url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(SIMPJT_crawling, url)
    return {"message": "Crawling started in the background"}