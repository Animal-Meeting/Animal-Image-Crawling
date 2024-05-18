from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
from selenium.webdriver.common.by import By




def get_image(search):
  
    if not os.path.isdir(search+ "/"):
        os.makedirs(search + "/")

    driver = webdriver.Chrome("./chromedriver") 
    driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

    elem = driver.find_element("name", "q")
    elem.send_keys(search)
    elem.send_keys(Keys.RETURN)

    SCROLL_PAUSE_TIME = 0.5

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:
                driver.find_element("css selector", ".mye4qd").click()
            except:
                break
        last_height = new_height

    images = driver.find_elements("css selector",".rg_i.Q4LuWd")
    count = 1

    print("The end")

    for image in images:
        try:
            image.click()
            time.sleep(SCROLL_PAUSE_TIME)
            #time.sleep(2)
            imgUrl = driver.find_element(By.XPATH, "//*[@id='Sva75c']/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]").get_attribute('src')
            urllib.request.urlretrieve(imgUrl, search +"/" + search + "_" + str(count) + ".jpg")
            print("Image saved: 여자강아지_{}.jpg".format(count))
            count += 1
            if count == 60:
                break
        except:
            print("error")
            pass

    driver.close()
    # //*[@id="islrg"]/div[1]/div[6]/a[1]/div[1]/img
    #//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img
    #//*[@id='Sva75c']/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img
    #   //*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]


search =["박보영", "블랙핑크 지수", "아이유", "아이즈원 안유진", "에스파 윈터", "여자아이들 우기", "위키미키 지수연", "이달의 소녀 츄", "체히블렛 유주", "프로미스나인 백지헌", "프로미스나인 장규리"]

for i in search:
    get_image(i)