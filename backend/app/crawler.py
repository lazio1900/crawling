### load package
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementClickInterceptedException
import time
import re
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal

### 전체 평수 구하기 함수
def all_width_make(driver):
    detail_sorting_width = driver.find_element(By.XPATH, '//*[@id="detailContents1"]/div[1]/table/tbody/tr[8]/td/div/div')
    all_width_str = detail_sorting_width.text
    width_list = [item.strip() for item in all_width_str.split(',')]
    try:
        driver.find_element(By.XPATH, '//*[@id="detailContents1"]/div[2]/div[2]/div/div[2]/button').click()
    except:
        pass
    return width_list

### 단지 내 면적별 정보 클릭하고 '매매', '전세', '월세', '단기' 값 추출 함수
def all_width_value_make(driver, i):
    tab_id = f"tab{i}"
    tab_element = driver.find_element(By.ID, tab_id)
    time.sleep(2)
    tab_element.click()
    info_table_item = driver.find_element(By.XPATH, '//*[@id="tabpanel"]/table/tbody/tr[5]')
    data_elements = info_table_item.find_elements(By.CLASS_NAME, 'data')
    results = []
    for data in data_elements:
        value = data.find_element(By.CLASS_NAME, 'point2').text
        results.append(value)
    return results

### 단지 ID로 URL 생성
# 단지 ID 는 url에 포함된 단지 ID 사용
# ex)
# https://new.land.naver.com/complexes/{complex_id}?ms=37.498319,127.0413807,16&a=APT:PRE:ABYG:JGC&e=RETAIL&ad=true
def make_url(complex_id):
    complex_id = complex_id
    url = f"https://new.land.naver.com/complexes/{complex_id}?ms=37.498319,127.0413807,16&a=APT:PRE:ABYG:JGC&e=RETAIL&ad=true"
    return url

# 단지 검색용 크롤링 (단지명, 세대수, 건설사, 주소, 평수)
def crawl_complex_info(complex_id):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.114 Safari/537.36")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    options.add_experimental_option("useAutomationExtension", False)


    info_result = {}

    url = make_url(complex_id)

    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    # 단지정보 열기
    complex_btn = driver.find_element(By.CLASS_NAME, 'complex_link')
    complex_btn.click()
    time.sleep(1)

    # 단지명
    complex_name = driver.find_element(By.XPATH, '//*[@id="complexTitle"]')
    complex_name_str = complex_name.text    

    # 세대수
    complex_num = driver.find_element(By.XPATH, '//*[@id="detailContents1"]/div[1]/table/tbody/tr[1]/td[1]')
    complex_num_str = complex_num.text    

    # 건설사
    complex_company = driver.find_element(By.XPATH, '//*[@id="detailContents1"]/div[1]/table/tbody/tr[4]/td')
    complex_company_str = complex_company.text

    # 주소
    complex_addr = driver.find_element(By.XPATH, '//*[@id="detailContents1"]/div[1]/table/tbody/tr[7]/td/p[1]')
    complex_addr_str = complex_addr.text
    
    # 평수
    complex_width = all_width_make(driver)

    info_result[complex_id] = {
        "complex_id": complex_id,
        "complex_name": complex_name_str,
        "complex_num": complex_num_str,
        "complex_company": complex_company_str,
        "complex_addr": complex_addr_str,
        "complex_width": complex_width
    }

    driver.quit()

    return info_result

# 단지별 디테일 크롤링 (평수별 매매 수 등)
def crawl_widthes_sales_info(complex_id):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.114 Safari/537.36")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    options.add_experimental_option("useAutomationExtension", False)

    # 크롤링 메타 정보부터 만들기
    crawl_meta_result = {}
    
    crawl_meta_result[complex_id] = {
        "execution_date": datetime.now(),
        "complex_id": complex_id,
        "status": 'pending',
        "attempt_count": 0,
    }

    # 평수별 매매 수 등 정보 크롤링
    detail_result = {}

    url = make_url(complex_id)

    success = False  # 성공 여부를 추적

    for attempt in range(1, 4):
        try:
            crawl_meta_result[complex_id]["attempt_count"] = attempt
            driver = webdriver.Chrome(options=options)
            # driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(5)

            # 단지정보 열기
            complex_btn = driver.find_element(By.CLASS_NAME, 'complex_link')
            complex_btn.click()
            time.sleep(1)

            # 평수 목록
            complex_width = all_width_make(driver)

            # 평수 만큼 정보 크롤링 반복
            width_sales_res = {}
            for idx, complex_width_ in enumerate(complex_width):

                tab_num = "tab" + str(idx)
                width_btn = driver.find_element(By.XPATH, f'//*[@id="{tab_num}"]/span')
                width_btn.click()
                    
                # 매매 수
                sales_count = driver.find_element(By.XPATH, '//*[@id="tabpanel"]/table/tbody/tr[5]/td/a[1]/span')
                sales_count_str = sales_count.text

                # 전세 수
                lease_count = driver.find_element(By.XPATH, '//*[@id="tabpanel"]/table/tbody/tr[5]/td/a[2]/span')
                lease_count_str = lease_count.text
                
                # 월세 수
                monthly_rent_count = driver.find_element(By.XPATH, '//*[@id="tabpanel"]/table/tbody/tr[5]/td/a[3]/span')
                monthly_rent_count_str = monthly_rent_count.text

                # 단기 수
                short_term_rent_count = driver.find_element(By.XPATH, '//*[@id="tabpanel"]/table/tbody/tr[5]/td/a[4]/span')
                short_term_rent_count_str = short_term_rent_count.text

                width_sales_res[complex_width_] = {
                    "complex_width": complex_width,
                    "sales_count": sales_count_str,
                    "lease_count": lease_count_str,
                    "monthly_rent_count": monthly_rent_count_str,
                    "short_term_rent_count": short_term_rent_count_str,            

                }
                
            # 크롤링이 성공했을 경우
            success = True
            detail_result = width_sales_res
            crawl_meta_result[complex_id]["status"] = "success"
            break  # 성공했으므로 반복 종료

        except (NoSuchElementException, WebDriverException, ElementClickInterceptedException) as e:
            print(f"에러 발생: {e}")
            # 에러 발생 시에도 계속 시도

        
        finally:
            if driver:
                driver.quit()

        # 3회 시도 후에도 실패한 경우
    if not success:
        crawl_meta_result[complex_id]["status"] = "failed"

    return crawl_meta_result, detail_result


# main 크롤링 코드
def SIMPJT_crawling(complex_id):
    url = make_url(complex_id)

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    complex_btn = driver.find_element(By.CLASS_NAME, 'complex_link')
    complex_btn.click()
    time.sleep(1)

    width_list = all_width_make(driver)

    last_result = []
    for i in range(len(width_list)):
        all_4_value = all_width_value_make(driver, i)
        all_4_value.insert(0, width_list[i])
        last_result.append(all_4_value)

    driver.quit()

    # 단지 ID 추출
    complex_id = extract_complex_id(url)

    db: Session = SessionLocal()
    try:
        complex_data = {
            "complex_id": complex_id,
            "complex_name": "Example Complex",
            "num_households": "100",
            "num_buildings": "5",
            "construction_date": "2023-01-01",
            "user_registration_date": datetime.now(),
            "url": url,
            "usage_status": "active",
        }

        crud.create_apartment_complex_basic(db, complex_data)

        for result in last_result:
            details_data = {
                "complex_id": complex_id,
                "size": result[0],
                "reference_date": datetime.now().date(),
                "sales_count": int(result[1]) if result[1].isdigit() else 0,
                "lease_count": int(result[2]) if result[2].isdigit() else 0,
                "monthly_rent_count": int(result[3]) if result[3].isdigit() else 0,
                "short_term_rent_count": int(result[4]) if result[4].isdigit() else 0,
            }
            crud.create_apartment_complex_details(db, details_data)

        crawling_data = {
            "execution_date": datetime.now(),
            "complex_id": complex_id,
            "status": "success",
            "attempt_count": i+1,
        }

        crud.create_crawling_data(db, crawling_data)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()
