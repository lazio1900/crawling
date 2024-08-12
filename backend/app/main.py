##### main.py
### FastAPI 설정
### 이 파일은 FastAPI 애플리케이션을 설정하고, API 엔드포인트를 정의합니다.

# Base.metadata.create_all(bind=engine): 데이터베이스 테이블을 생성합니다.
# app = FastAPI(): FastAPI 애플리케이션을 생성합니다.
# API 엔드포인트: 데이터베이스에 데이터를 추가하는 API를 정의합니다.
# get, post, patch, put, delete

from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from crawler import SIMPJT_crawling, crawl_complex_info

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 단지 등록시 ID 받아온 뒤 단지 확인 엔드포인트
@app.post("/complex_search/")
def complex_info_search(complex_id: dict, db: Session = Depends(get_db)):
    print(complex_id["complexId"])
    # cralwing
    search_res = crawl_complex_info(complex_id["complexId"])
    return search_res



# apartment_complex_basic Table 생성
@app.post("/apartment-complex/")
def create_apartment_complex(complex_data: dict, db: Session = Depends(get_db)):
    print(complex_data["complexId"])
    # cralwing
    return {"message": "굳"}

# apartment_complex_details Table 생성
@app.post("/apartment-complex/details/")
def create_apartment_complex_details(details_data: dict, db: Session = Depends(get_db)):
    return 

# create_crawling_data Table 생성
@app.post("/crawling-data/")
def create_crawling_data(crawling_data: dict, db: Session = Depends(get_db)):
    return

# crawl 실행
@app.post("/crawl/")
def trigger_crawling(url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(SIMPJT_crawling, url)
    return {"message": "Crawling started in the background"}