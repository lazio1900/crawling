##### crud.py
### crud 기능 추가
### 이 파일은 데이터베이스에서 기본적인 CRUD 작업을 수행하는 함수를 정의합니다

# create_apartment_complex_basic: apartment_complex_basic 테이블에 데이터를 추가합니다.
# create_apartment_complex_details: apartment_complex_details 테이블에 데이터를 추가합니다.
# create_crawling_data: crawling_data 테이블에 데이터를 추가합니다.

from sqlalchemy.orm import Session
from app import models

# 단지기본 정보 생성 함수
def create_apartment_complex_basic(db: Session, complex_data):
    db_complex = models.ApartmentComplexBasic(**complex_data)
    db.add(db_complex)
    db.commit()
    db.refresh(db_complex)
    return db_complex

# 단지상세 정보 생성 함수
def create_apartment_complex_details(db: Session, details_data):
    db_details = models.ApartmentComplexDetails(**details_data)
    db.add(db_details)
    db.commit()
    db.refresh(db_details)
    return db_details

# 크롤링 데이터 생성 함수
def create_crawling_data(db: Session, crawling_data):
    db_crawl = models.CrawlingData(**crawling_data)
    db.add(db_crawl)
    db.commit()
    db.refresh(db_crawl)
    return db_crawl
