from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import json
import time

from datetime import datetime


USER_PROFILE_SRC = "./user_profiles.json"
REFRESH_RATE = 60
eps = 10
delay = 0.1
course_id = 'B3J063240'
target_time = datetime(2020, 9, 8, 0, 17, 00)

# load user profiles
with open(USER_PROFILE_SRC, "r") as f:
    user_profiles = json.load(f)

# initialize
browser = webdriver.Chrome(user_profiles["DRIVER_PATH"])
wait = WebDriverWait(browser, 5)
browser.get("http://jwxt.buaa.edu.cn:7001/ieas2.1")

# goto login page
browser.find_element_by_xpath('//*[@id="notice"]/div[2]/div[1]/p[2]/input').click()
wait.until(EC.frame_to_be_available_and_switch_to_it(browser.find_element_by_id('loginIframe')))

# login
browser.find_element_by_id("unPassword").send_keys(user_profiles["USER_NAME"])
browser.find_element_by_id("pwPassword").send_keys(user_profiles["USER_PASSWORD"])
browser.find_element_by_xpath('//*[@id="content-con"]/div[1]/div[7]/input').click()

while True:
    browser.get('http://jwxt.buaa.edu.cn:7001/ieas2.1/xslbxk/queryYxkc?pageXklb=xslbxk')
    browser.find_element_by_xpath('//*[@id="queryform"]/ul/li[3]/div/a').click()
    curr_time = datetime.now()
    diff = (target_time - curr_time).total_seconds()

    if diff > REFRESH_RATE + eps:
        time.sleep(REFRESH_RATE)
    else:
        time.sleep(diff)
        browser.find_element_by_xpath('//*[@id="2020-2021-1-' + course_id + '-001"]').click()
        try:
            browser.switch_to.alert.accept()
            print("time: " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            print("course released")
            browser.switch_to.alert.accept()
        except:
            print("failed")
        break


