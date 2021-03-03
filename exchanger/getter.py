from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

import json
import time
import requests

from datetime import datetime


USER_PROFILE_SRC = "./user_profiles.json"
RESTART_DELAY_AVG = 60
REFRESH_RATE = 300
MAX_RETRY = 100
RETRY_BREAK = 0.5
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

# login and get cookies
browser.find_element_by_id("unPassword").send_keys(user_profiles["USER_NAME"])
browser.find_element_by_id("pwPassword").send_keys(user_profiles["USER_PASSWORD"])
browser.find_element_by_xpath('//*[@id="content-con"]/div[1]/div[7]/input').click()
cookies = {}
for cookie in browser.get_cookies():
    cookies[cookie['name']] = cookie['value']
browser.close()


list_url = 'http://jwxt.buaa.edu.cn:7001/ieas2.1/xslbxk/queryXsxkList?pageXkmkdm=ZYL'
save_url = 'http://jwxt.buaa.edu.cn:7001/ieas2.1/xslbxk/saveXsxk'
formdata_heads_validations = ['kcdmpx', 'kcmcpx', 'rlpx',
                              'zy', 'qz', 'token', 'pageKclb', 'pageXklb', 'pageXkmkdm']
print("schedualed to exchange @ " + target_time.strftime("%Y-%m-%d_%H-%M-%S"))
while True:
    curr_time = datetime.now()
    diff = (target_time - curr_time).total_seconds()

    if diff > REFRESH_RATE + eps:
        time.sleep(REFRESH_RATE)
    else:
        time.sleep(diff)
        cnt = 0
        while cnt < MAX_RETRY:
            # load query tokens
            response = requests.get(list_url, cookies=cookies)
            query_html = BeautifulSoup(response.text)
            data = {'pageXnxq': user_profiles["SEMESTER"][:-2]+user_profiles["SEMESTER"][-1],
                    'pageKkxiaoqu': '',
                    'pageKkyx': '06',
                    'pageKcmc': '',
                    'pageYcctkc': '1'}
            for h in formdata_heads_validations:
                data[h] = query_html.find_all(id=h)[0].attrs['value']

            # make query
            data['rwh'] = f"{user_profiles['SEMESTER']}-{course_id}-001"
            response = requests.post(save_url, data=data, cookies=cookies)

            # check status
            if not ("选课成功" in response.text or "容量已满，请选择其它课程！" in response.text):
                with open("response.html", "w") as f:
                    f.write(response.text)
                raise ConnectionError(
                    "Error occurs, response is saved to 'response.html'")

            # finalize
            if "选课成功" in response.text:
                print("success")
                break
            print(f"round {cnt:04d} | time: {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')} | success: {'选课成功' in response.text}")
            time.sleep(RETRY_BREAK)
        if cnt >= MAX_RETRY:
            print("failed")
        break
