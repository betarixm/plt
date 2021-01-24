#-*- coding:utf-8 -*- 
import sys
from selenium import webdriver
import time

def check_alert(URI):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
        options.add_argument('disable-gpu')    # GPU 사용 안함
        options.add_argument('lang=ko_KR')    # 언어 설정
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)
        print(URI)
        driver.get(URI)
        try:
            driver.implicitly_wait(2)
            alert = driver.switch_to_alert()
            alert.accept()
            driver.quit()
            return True, True
        except:
            driver.quit()
            return True, False

    except Exception as ex:
        print(ex)
        return False, False