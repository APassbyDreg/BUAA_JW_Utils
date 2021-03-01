from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import json
import time

from datetime import datetime


USER_PROFILE_SRC = "./user_profiles.json"
REFRESH_RATE = 300
eps = 15
delay = 0.1

# load user profiles
with open(USER_PROFILE_SRC, "r") as f:
    user_profiles = json.load(f)

# initialize
course_id = user_profiles["COURSE_ID"]
time_list = user_profiles["TIME"]
target_time = datetime(time_list[0],time_list[1],time_list[2],time_list[3],time_list[4],time_list[5])
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
    browser.get('http://jwxt.buaa.edu.cn:7001/ieas2.1/xslbxk/queryXsxk?pageXkmkdm=ZYL')
    browser.find_element_by_xpath('/html/body/div[7]/div/div[3]/table/tbody/tr/td[1]/ul/li[2]/a').click()
    select_college = 'document.getElementById("pageKkyxid").value = {};'.format(user_profiles["COLLEGE"])
    browser.execute_script(select_college)
    avoid_conflicts = 'document.getElementsByName("pageYcctkc")[0].checked = true;'
    browser.execute_script(avoid_conflicts)

    curr_time = datetime.now()
    diff = (target_time - curr_time).total_seconds()

    if diff > REFRESH_RATE + eps:
        time.sleep(REFRESH_RATE)
    else:
        print("loaded, schedualed to exchange @ " + target_time.strftime("%Y-%m-%d_%H-%M-%S"))
        time.sleep(diff + delay)
        browser.execute_script('queryLike()')
        select_course = 'saveXsxk("' + user_profiles["SEMESTER"] + '-' + course_id + '-001");'
        browser.execute_script(select_course)
        redo = False
        try:
            print("time: " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            print("result: " + browser.switch_to.alert.text)
            if browser.switch_to.alert.text[0] != '选':
                redo = True
            browser.switch_to.alert.accept()
        except:
            print("failed")
            redo = True
        if not redo:
            break
