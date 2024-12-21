from datetime import datetime

from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from crawler import SIMPJT_crawling, crawl_complex_info, crawl_widthes_sales_info
from crud import *
from apscheduler.schedulers.background import BackgroundScheduler

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

# 크롤링한 apply 정보를 받는 엔드포인트
@app.post("/complex_apply/")
def complex_info_apply(complex_info: dict, db: Session = Depends(get_db)):
    print(complex_info)

    complex_info['user_registration_date'] = datetime.now()
    complex_id = complex_info['complex_id']
    complex_info['url'] = f"https://new.land.naver.com/complexes/{complex_id}?ms=37.498319,127.0413807,16&a=APT:PRE:ABYG:JGC&e=RETAIL&ad=true"
    complex_info['usage_status'] = "Y"

    search_res = create_apartment_complex_basic(db, complex_info)

    
    return search_res

# 저정한 단지 Table을 랜더링 하는 엔드포인트
@app.post("/complex_list/")
def complex_info_list(db: Session = Depends(get_db)):
    return select_apartment_complex_basic(db)

### 단지 디테일 스케줄 기능 추가
# 단지 디테일 크롤링 결과 저장
def comp_detail_crawl_job():
    gen = get_db()
    db = gen.__next__()
    print("get_db ok")
    # 보유한 단지 단지번호 가져오기
    comps = select_apartment_complex_basic(db)
    print("comps 가져오는 중")
    print(comps)

    for comp in comps:
        # 단지 디테일 크롤링 및 DB add
        print("comp detail 진행중")
        _, detail_res = crawl_widthes_sales_info(comp.complex_id)
        print("detail_res : ", detail_res)
        add_detail_complexes(db, detail_res)

# 스케줄 객체 생성
sched = BackgroundScheduler(timezone='Asia/Seoul')  # 시간대 설정

sched.add_job(
    comp_detail_crawl_job,
    'cron',
    day_of_week='sat',
    hour='17',
    minute='20',
    id='test'
)  # 매주 금요일 수행
sched.start() #스케쥴링 작업 실행




# 크롤링 결과, 설정 및 시각화 페이지 엔드포인트
# @app.post("/complex_crawl_basic/")
# def crawl_page_basic(단지ID, db: Session = Depends(get_db)):
#     단지명
#     단지ID
#     최종크롤링 일자
#     단지ID의 히스토리 테이블
#     주기설정(매일, 매주, 매월 설정 가능)
#     return select_apartment_complex_basic(db)

# # apartment_complex_basic Table 생성
# @app.post("/apartment-complex/")
# def create_apartment_complex(complex_data: dict, db: Session = Depends(get_db)):
#     print(complex_data["complexId"])
#     # cralwing
#     return {"message": "굳"}

# # apartment_complex_details Table 생성
# @app.post("/apartment-complex/details/")
# def create_apartment_complex_details(details_data: dict, db: Session = Depends(get_db)):
#     return 

# # create_crawling_data Table 생성
# @app.post("/crawling-data/")
# def create_crawling_data(crawling_data: dict, db: Session = Depends(get_db)):
#     return

# # crawl 실행
# @app.post("/crawl/")
# def trigger_crawling(url: str, background_tasks: BackgroundTasks):
#     background_tasks.add_task(SIMPJT_crawling, url)
#     return {"message": "Crawling started in the background"}