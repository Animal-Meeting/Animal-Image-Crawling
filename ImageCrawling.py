from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_image(title, search):
  
    if not os.path.isdir("./image/" + search+ "/"):
        os.makedirs("./image/" + search + "/")

    # Chromedriver 경로 설정
    chrome_driver_path = "./chromedriver"  # 절대 경로로 변경
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 필요한 경우 헤드리스 모드
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 서비스 설정
    service = Service(chrome_driver_path)
    
    # 드라이버 초기화
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
    
    elem = driver.find_element("name", "q")
    elem.send_keys(search)
    elem.send_keys(Keys.RETURN)

    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 페이지 끝까지 내리기
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:
                driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
            except:
                break
        last_height = new_height

    # 페이지내 이미지들 선택
    images = driver.find_elements(By.CSS_SELECTOR, ".czzyk.XOEbc")
 
    count = 1

    print(f"Number of images found: {len(images)}")

    # 이미지 스크롤링
    for image in images:
        try:
            image.click()
            time.sleep(SCROLL_PAUSE_TIME)
            image_element = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]')
            imgUrl = image_element.get_attribute('src')
            
            imgUrl = imgUrl.replace('https', 'http') # https로 요청할 경우 보안 문제로 SSL에러가 남
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            
            urllib.request.urlretrieve(imgUrl, "./image/" + search +"/" + search + "_" + str(count) + ".jpg")
            print("Image saved: " + title + "_{}.jpg".format(count))
            count += 1
            if count == 100:
                break
        except:
            print("error")
            pass

    driver.quit()
    
title = "여자강아지"
search =["블랙핑크 지수 얼굴"]

for i in search:
    get_image(title, i)
    