from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import json
import time
import random

from datetime import datetime


USER_PROFILE_SRC = "./user_profiles.json"
REFRESH_RATE = 300
eps = 15
delay = 0.1

# load user profiles
with open(USER_PROFILE_SRC, "r") as f:
    user_profiles = json.load(f)

# initialize
browser = webdriver.Chrome(user_profiles["DRIVER_PATH"])
wait = WebDriverWait(browser, 5)

# goto login page
browser.get("https://sso.buaa.edu.cn/login?service=http%3A%2F%2Fjwxt.buaa.edu.cn%3A8081%2Fieas2.1%2Fwelcome%3Ffalg%3D1")
wait.until(EC.frame_to_be_available_and_switch_to_it(browser.find_element_by_id('loginIframe')))

# login
browser.find_element_by_id("unPassword").send_keys(user_profiles["USER_NAME"])
browser.find_element_by_id("pwPassword").send_keys(user_profiles["USER_PASSWORD"])
browser.find_element_by_xpath('//*[@id="content-con"]/div[1]/div[7]/input').click()

# nav to score page
browser.get("http://jwxt.buaa.edu.cn:8081/ieas2.1/xspj/Fxpj_fy")

# all teachers
elems = browser.find_elements_by_xpath('//*[@id="queryform"]/div[3]/table/tbody/*/td[6]/span[1]/*')
while len(elems) > 0:
    curr = elems.pop(0)
    curr.click()

    # score
    numcols = len(browser.find_elements_by_xpath('//*[@id="zbtable"]/tbody/tr')) - 2
    for i in range(numcols):
        if user_profiles["RATE"] == 0:
            score = random.randint(1, 3)
        elif user_profiles["RATE"] == 1:
            score = 1
        elif user_profiles["RATE"] == -1:
            score = 4
        else:
            raise ValueError(f'"RATE" should be -1, 0 or 1, current value [{user_profiles["RATE"]}] is invalid')
        # offset first score
        if i == 0:
            score += user_profiles["RATE"]
        first = browser.find_element_by_xpath(f'//*[@id="zbtable"]/tbody/tr[{i+2}]/td[3]/input[{score}]').click()

    # recommend
    if user_profiles['RATE'] >= 0:
        browser.execute_script("document.getElementsByName('sftj')[0].value = 1")
    else:
        browser.execute_script("document.getElementsByName('sftj')[0].value = 2")

    # submit
    browser.find_element_by_xpath('//*[@id="bt"]').click()
    browser.switch_to.alert.accept()
    time.sleep(1)
    browser.switch_to.alert.accept()

    elems = browser.find_elements_by_xpath('//*[@id="queryform"]/div[3]/table/tbody/*/td[6]/span[1]/*')

print("finished")
