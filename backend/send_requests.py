import requests

url = "http://127.0.0.1:8000/crawl/"
params = {"url": "https://new.land.naver.com/complexes/11698?ms=37.498319,127.0413807,16&a=APT:PRE:ABYG:JGC&e=RETAIL&ad=true"}

response = requests.post(url, params=params)
print(response.json())
