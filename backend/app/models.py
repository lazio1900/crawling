##### models.py
### 모델 정의
### 데이터베이스 테이블을 나타내는 SQLALchemy 모델을 정의

# ApartmentComplexBasic: apartment_complex_basic 테이블을 나타내는 모델입니다.
# ApartmentComplexDetails: apartment_complex_details 테이블을 나타내는 모델입니다.
# CrawlingData: crawling_data 테이블을 나타내는 모델입니다.

from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# 기본 정보 테이블 모델
class ApartmentComplexBasic(Base):
    __tablename__ = "apartment_complex_basic"

    complex_id = Column(String, primary_key=True, index=True)
    complex_name = Column(String)
    num_households = Column(String)
    num_buildings = Column(String)
    construction_date = Column(Date)
    user_registration_date = Column(TIMESTAMP)
    url = Column(String)
    usage_status = Column(String)

    details = relationship("ApartmentComplexDetails", back_populates="complex")
    crawls = relationship("CrawlingData", back_populates="complex")

# 상세 정보 테이블 모델
class ApartmentComplexDetails(Base):
    __tablename__ = "apartment_complex_details"

    complex_id = Column(String, ForeignKey("apartment_complex_basic.complex_id"), primary_key=True)
    size = Column(String, primary_key=True)
    reference_date = Column(Date, primary_key=True)
    sales_count = Column(Integer)
    lease_count = Column(Integer)
    monthly_rent_count = Column(Integer)
    short_term_rent_count = Column(Integer)

    complex = relationship("ApartmentComplexBasic", back_populates="details")

# 크롤링 데이터 테이블 모델
class CrawlingData(Base):
    __tablename__ = "crawling_data"

    crawling_id = Column(Integer, primary_key=True, autoincrement=True)
    execution_date = Column(TIMESTAMP, primary_key=True)
    complex_id = Column(String, ForeignKey("apartment_complex_basic.complex_id"))
    status = Column(String)
    attempt_count = Column(Integer)

    complex = relationship("ApartmentComplexBasic", back_populates="crawls")
