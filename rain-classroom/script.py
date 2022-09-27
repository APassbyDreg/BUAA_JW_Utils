from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import time
import os

driver = webdriver.Edge(os.path.join(os.path.abspath("."), "msedgedriver.exe"))
driver.get(os.path.join(os.path.abspath("."), "index.html"))

from tqdm import trange
for _ in trange(60):
    time.sleep(1)

base_window = driver.current_window_handle
course_list = driver.find_elements(By.CLASS_NAME, "progress-wrap")

for i, item in enumerate(course_list):
    if "已" not in item.text and item.text != "未发言":
        # 打开并转换到新页面
        ActionChains(driver).click(item).perform()
        for window_handle in driver.window_handles:
            if window_handle != base_window:
                driver.switch_to.window(window_handle)
                break
        time.sleep(2)
        
        # 等待结束
        if len(driver.find_elements(By.TAG_NAME, "video")) > 0:
            done = False
            title = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[3]/div/div[2]/div/div/section[1]/div[1]/span').text
            while not done:
                # 检测完成度
                try:
                    progress = driver.find_elements(By.CLASS_NAME, "progress-wrap")[0].text
                    done = done or ("完成度：100%" == progress)
                except:
                    progress = "unknown"
                # 检测进度条时间
                try:
                    timer = driver.find_element(By.TAG_NAME, "xt-time")
                    tcurr = timer.find_element(By.XPATH, "./span[1]").text
                    tfull = timer.find_element(By.XPATH, "./span[2]").text
                    done = done or (len(tcurr) > 0 and len(tfull) > 0 and tfull != "00:00:00" and tcurr == tfull)
                except:
                    pass
                # 停一会
                time.sleep(2)
                print(title, "|", progress)
        
        # 回到列表
        driver.close()
        driver.switch_to.window(base_window)
        
    print(f"已完成 {i + 1} / {len(course_list)}")
            
            


